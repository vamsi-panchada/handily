from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.services.tool_service import ToolService
from app.schemas.tool import ToolResponse, ToolCreate, ToolUpdate
from app.models.tool import ToolCategory

router = APIRouter()

@router.get("/tools", response_model=List[ToolResponse])
async def list_tools(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[ToolCategory] = None,
    search: Optional[str] = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get list of available tools with optional filtering.
    """
    return await ToolService.get_tools(
        db, skip, limit, category, search, active_only
    )

@router.get("/tools/{tool_id}", response_model=ToolResponse)
async def get_tool(
    tool_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific tool by ID.
    """
    return await ToolService.get_tool_by_id(db, tool_id)

@router.post("/tools", response_model=ToolResponse)
async def create_tool(
    tool_data: ToolCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new tool.
    """
    return await ToolService.create_tool(db, tool_data)

@router.patch("/tools/{tool_id}", response_model=ToolResponse)
async def update_tool(
    tool_id: int,
    tool_data: ToolUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing tool.
    """
    return await ToolService.update_tool(db, tool_id, tool_data)