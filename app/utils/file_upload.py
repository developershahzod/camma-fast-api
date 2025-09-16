import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from ..core.config import settings

ALLOWED_EXTENSIONS = {
    'image': {'.jpg', '.jpeg', '.png', '.gif'},
    'document': {'.pdf', '.doc', '.docx'},
    'video': {'.mp4', '.avi', '.mov'}
}

def get_file_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def validate_file(file: UploadFile, file_type: str) -> bool:
    if file_type not in ALLOWED_EXTENSIONS:
        return False
    
    extension = get_file_extension(file.filename)
    return extension in ALLOWED_EXTENSIONS[file_type]

async def save_upload_file(file: UploadFile, directory: str, file_type: str) -> str:
    if not validate_file(file, file_type):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
    
    # Create directory if it doesn't exist
    upload_path = os.path.join(settings.UPLOAD_DIR, directory)
    os.makedirs(upload_path, exist_ok=True)
    
    # Generate unique filename
    file_extension = get_file_extension(file.filename)
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"
    file_path = os.path.join(upload_path, unique_filename)
    
    # Save file
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    
    return file_path