"""

"""

from pathlib import Path
from fastapi import APIRouter, UploadFile, HTTPException

UPLOAD_CONTROLLER = APIRouter(prefix="/page/file")


@UPLOAD_CONTROLLER.post("/upload")
async def upload_file(file: UploadFile):
    if file.filename is None:
        raise HTTPException(status_code=400, detail="File name is required")

    if file.content_type not in [
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

    file_path = Path("uploads") / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {"filename": file.filename}
