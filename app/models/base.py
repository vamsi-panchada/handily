from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ResponseBase(BaseModel):
    success: bool
    message: str
    error: Optional[str] = None

class ToolResponse(ResponseBase, Generic[T]):
    data: Optional[T] = None