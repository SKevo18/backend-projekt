from pathlib import Path

from db import get_db
from db.orm import Page, User
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pathvalidate import sanitize_filename, validate_filename
from sqlalchemy.orm import Session

from controllers.dependencies import get_current_user
from controllers.page_controller import check_can_edit_page

UPLOAD_CONTROLLER = APIRouter(prefix="/page/{page_id}/upload")
FILE_UPLOAD_MAX_MB = 10


def validate_file_name(filename: str):
    try:
        validate_filename(filename)
        safe_filename = sanitize_filename(filename)

        if not safe_filename:
            raise HTTPException(
                status_code=400, detail="Invalid file name after sanitization."
            )
        return safe_filename
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid file name: {str(e)}")


def validate_file(uploaded_file: UploadFile):
    if not uploaded_file.filename:
        raise HTTPException(status_code=400, detail="File name is required")

    uploaded_file.filename = validate_file_name(uploaded_file.filename)

    if uploaded_file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/gif",
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ]:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    if (
        uploaded_file.size is None
        or uploaded_file.size > FILE_UPLOAD_MAX_MB * 1024 * 1024
    ):
        raise HTTPException(status_code=400, detail="File is too large (max: 10 MB).")

    return uploaded_file


@UPLOAD_CONTROLLER.get("/")
def list_files(page_id: int, db: Session = Depends(get_db)):
    page = db.query(Page).filter(Page.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found.")

    upload_dir = Path("uploads") / str(page_id)
    if not upload_dir.exists():
        return []

    files = []
    for file_path in upload_dir.iterdir():
        if file_path.is_file():
            files.append(
                {
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "uri": f"uploads/{page_id}/{file_path.name}",
                }
            )

    return files


@UPLOAD_CONTROLLER.post("/")
def upload_file(
    page_id: int,
    uploaded_file: UploadFile = Depends(validate_file),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found.")

    check_can_edit_page(current_user, page_id, db)

    file_path = Path("uploads") / str(page_id) / uploaded_file.filename  # type: ignore
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("wb") as f:  # will overwrite existing file
        f.write(uploaded_file.file.read())

    return {"uri": f"uploads/{page_id}/{uploaded_file.filename}"}


@UPLOAD_CONTROLLER.get("/{filename}")
def get_file(page_id: int, filename: str = Depends(validate_file_name)):
    file_path = Path("uploads") / str(page_id) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(file_path)


@UPLOAD_CONTROLLER.delete("/{filename}")
def delete_file(
    page_id: int,
    filename: str = Depends(validate_file_name),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found.")

    check_can_edit_page(current_user, page_id, db)

    file_path = Path("uploads") / str(page_id) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    file_path.unlink()
