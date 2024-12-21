from pydantic import BaseModel
from typing import Optional
from ..models.tool import ToolCategory
from datetime import datetime

class ToolBase(BaseModel):
    name: str
    description: str
    category: ToolCategory
    icon: str
    endpoint: str
    is_active: bool = True

class ToolCreate(ToolBase):
    pass

class ToolUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ToolCategory] = None
    icon: Optional[str] = None
    endpoint: Optional[str] = None
    is_active: Optional[bool] = None

class ToolResponse(ToolBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True