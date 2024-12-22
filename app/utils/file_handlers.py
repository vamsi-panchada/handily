import shutil
import uuid
import os
from pathlib import Path
from typing import List, Optional, Set
from fastapi import UploadFile, HTTPException
from app.core.config import settings
from app.core.exceptions import FileValidationError
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class FileValidator:
    """Utility class for file validation"""
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int) -> bool:
        """Check if file size is within limits"""
        return file_size <= max_size
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: Set[str]) -> bool:
        """Check if file extension is allowed"""
        return any(filename.lower().endswith(ext) for ext in allowed_extensions)

class FileManager:
    """Class to manage file operations"""
    
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        self._ensure_upload_directory()
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def _ensure_upload_directory(self) -> None:
        """Ensure upload directory exists with proper permissions"""
        try:
            self.upload_dir.mkdir(parents=True, exist_ok=True)
            # Set directory permissions to 755
            self.upload_dir.chmod(0o755)
        except Exception as e:
            logger.error(f"Failed to create upload directory: {str(e)}")
            raise FileValidationError("Failed to initialize file storage system")
    
    def _generate_unique_filename(self, original_filename: str) -> str:
        """Generate a unique filename while preserving extension"""
        ext = Path(original_filename).suffix
        return f"{uuid.uuid4().hex}{ext}"
    
    async def _write_file(self, file_path: Path, file: UploadFile) -> None:
        """Write file to disk asynchronously"""
        try:
            # Use ThreadPoolExecutor for file I/O operations
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                self.executor,
                self._write_file_sync,
                file_path,
                file
            )
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {str(e)}")
            raise FileValidationError(f"Failed to save file: {str(e)}")
    
    def _write_file_sync(self, file_path: Path, file: UploadFile) -> None:
        """Synchronous file writing operation"""
        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        finally:
            file.file.close()
    
    def _validate_file(
        self,
        file: UploadFile,
        allowed_extensions: Optional[List[str]] = None,
        max_size: Optional[int] = None
    ) -> None:
        """Validate file before saving"""
        if allowed_extensions:
            if not FileValidator.validate_file_extension(file.filename, set(allowed_extensions)):
                raise FileValidationError(
                    f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
                )
        
        # Get file size
        try:
            file_size = 0
            file.file.seek(0, 2)  # Seek to end of file
            file_size = file.file.tell()
            file.file.seek(0)  # Reset file position
            
            if max_size and not FileValidator.validate_file_size(file_size, max_size):
                raise FileValidationError(
                    f"File size exceeds maximum allowed size of {max_size/1024/1024:.1f}MB"
                )
        except Exception as e:
            logger.error(f"Error validating file size: {str(e)}")
            raise FileValidationError("Failed to validate file size")

async def save_upload_file(
    upload_file: UploadFile,
    allowed_extensions: Optional[List[str]] = None,
    max_size: Optional[int] = None,
    custom_filename: Optional[str] = None
) -> Path:
    """
    Save uploaded file and return the path
    
    Args:
        upload_file: FastAPI UploadFile object
        allowed_extensions: List of allowed file extensions (e.g., ['.pdf', '.txt'])
        max_size: Maximum allowed file size in bytes
        custom_filename: Optional custom filename to use instead of generated one
    
    Returns:
        Path: Path to the saved file
    
    Raises:
        FileValidationError: If file validation fails
        HTTPException: If file operations fail
    """
    try:
        file_manager = FileManager()
        
        # Validate file
        file_manager._validate_file(
            upload_file,
            allowed_extensions,
            max_size
        )
        
        # Generate or use custom filename
        filename = custom_filename or file_manager._generate_unique_filename(upload_file.filename)
        file_path = file_manager.upload_dir / filename
        
        # Save file
        await file_manager._write_file(file_path, upload_file)
        
        logger.info(f"Successfully saved file: {filename}")
        return file_path
    
    except FileValidationError as e:
        logger.error(f"File validation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

async def cleanup_file(file_path: Path) -> None:
    """
    Remove temporary file safely
    
    Args:
        file_path: Path to the file to be removed
    
    Raises:
        HTTPException: If file cleanup fails
    """
    if not file_path:
        return
        
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            ThreadPoolExecutor(),
            _cleanup_file_sync,
            file_path
        )
        logger.info(f"Successfully cleaned up file: {file_path}")
    except Exception as e:
        logger.error(f"Failed to cleanup file {file_path}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cleanup file: {str(e)}"
        )

def _cleanup_file_sync(file_path: Path) -> None:
    """Synchronous file cleanup operation"""
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        logger.error(f"Error in synchronous file cleanup: {str(e)}")
        raise