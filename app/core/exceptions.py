from fastapi import HTTPException
from typing import Any

class ToolException(HTTPException):
    def __init__(self, detail: Any = None, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)

class FileValidationError(ToolException):
    pass

class ProcessingError(ToolException):
    pass