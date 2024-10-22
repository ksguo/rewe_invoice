from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
import os
import aiofiles
from typing import List
from app.db.database import get_db
from app.db.models import User, Purchase
from app.user_management.router import get_current_active_user
from app.db.crud import create_record, read_records, delete_record, update_record

router = APIRouter()


# File management
@router.post(
    "/upload-files",
    status_code=status.HTTP_201_CREATED,
    summary="Upload files",
    description="Allows for the uploading and saving of multiple PDF or image files.",
    tags=["file_management"],
    responses={
        201: {"description": "Files uploaded successfully"},
        400: {"description": "Bad Request: Unsupported file type"},
    },
)
async def upload_files(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_active_user),
):
    saved_files = []
    with get_db() as db:
        for file in files:
            if not (
                file.content_type == "application/pdf"
                or file.content_type.startswith("image/")
            ):
                raise HTTPException(
                    status_code=400, detail="Only PDF and image files are supported"
                )
            new_purchase = create_record(
                db,
                Purchase,
                user_id=current_user.user_id,
                file_name=file.filename,
                file_path="",
            )  # Placeholder for now
            file_location = f"uploaded_invoices/{current_user.user_id}-{new_purchase.purchase_id}-{file.filename}"
            os.makedirs(os.path.dirname(file_location), exist_ok=True)
            async with aiofiles.open(file_location, mode="wb") as buffer:
                while data := await file.read(1024):
                    await buffer.write(data)
            update_record(
                db, Purchase, new_purchase.purchase_id, file_path=file_location
            )
            saved_files.append(
                f"{current_user.user_id}-{new_purchase.purchase_id}-{file.filename}"
            )
    return {"saved_files_purchase_id": saved_files}


@router.get(
    "/list-user-files",
    summary="List all files for a user",
    description="Lists all files uploaded by the current user.",
    tags=["file_management"],
    responses={
        200: {"description": "Files retrieved successfully"},
        404: {"description": "No files found for user"},
    },
)
async def list_user_files(current_user: User = Depends(get_current_active_user)):
    with get_db() as db:
        files = read_records(db, Purchase, filters={"user_id": current_user.user_id})
    if not files:
        raise HTTPException(status_code=404, detail="No files found for this user.")
    file_list = [
        {
            "file_id": file.purchase_id,
            "file_name": file.file_name,
            "file_path": file.file_path,
        }
        for file in files
    ]
    return {"files": file_list}


@router.delete(
    "/files/{file_id}",
    summary="Delete a file",
    description="Deletes a specific file uploaded by the current user.",
    tags=["file_management"],
    responses={
        200: {"description": "File deleted successfully"},
        404: {"description": "File not found"},
        403: {"description": "Forbidden: Not allowed to delete this file"},
        500: {"description": "Internal Server Error"},
    },
)
async def delete_user_file(
    file_id: int, current_user: User = Depends(get_current_active_user)
):
    with get_db() as db:
        file_check = read_records(
            db,
            Purchase,
            filters={"user_id": current_user.user_id, "purchase_id": file_id},
            limit=1,
        )
        if not file_check:
            raise HTTPException(
                status_code=404,
                detail="File not found in database or not owned by user",
            )
        file_to_delete = file_check[0]
        if file_to_delete.user_id != current_user.user_id:
            raise HTTPException(
                status_code=403, detail="Forbidden: Not allowed to delete this file"
            )
        file_path = file_to_delete.file_path
        file_name = file_to_delete.file_name
        if os.path.exists(file_path):
            os.remove(file_path)
        delete_record(db, Purchase, file_id)
        return {"message": f"File '{file_name}' deleted successfully"}
