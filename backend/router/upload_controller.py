import re
from pathlib import Path

from db import get_db
from db.orm import Page
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

UPLOAD_CONTROLLER = APIRouter(prefix="/page/{page_id}/upload")

# HACK: temporary, look up proper way how to validate file name
FILENAME_RGX = re.compile(r"^[\w\.-]+$")


def validate_file_name(filename: str):
    if FILENAME_RGX.match(filename):
        return filename
    else:
        raise HTTPException(status_code=400, detail="Invalid file name.")


def validate_file(uploaded_file: UploadFile):
    if not validate_file_name(uploaded_file.filename or ""):
        raise HTTPException(status_code=400, detail="File name is required")

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

    if uploaded_file.size is None or uploaded_file.size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=400, detail="File is too large.")

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
):
    page = db.query(Page).filter(Page.id == page_id).first()
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found.")

    file_path = Path("uploads") / str(page_id) / uploaded_file.filename  # type: ignore
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("wb") as f:  # will overwrite existing file
        f.write(uploaded_file.file.read())

    return {"uri": f"uploads/{page_id}/{uploaded_file.filename}"}


@UPLOAD_CONTROLLER.get("/{filename}")
async def get_file(page_id: int, filename: str = Depends(validate_file_name)):
    file_path = Path("uploads") / str(page_id) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(file_path)


@UPLOAD_CONTROLLER.delete("/{filename}")
async def delete_file(page_id: int, filename: str = Depends(validate_file_name)):
    file_path = Path("uploads") / str(page_id) / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found.")
    file_path.unlink()
