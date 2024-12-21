from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.tool import Tool, ToolCategory
from ..schemas.tool import ToolUpdate, ToolCreate
from fastapi import HTTPException

class ToolService:

    @staticmethod
    async def get_tools(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[ToolCategory] = None,
        search: Optional[str] = None,
        active_only: bool = True
    ) -> List[Tool]:
        query = db.query(Tool)
        
        if category:
            query = query.filter(Tool.category == category)
        
        if search:
            query = query.filter(
                Tool.name.ilike(f"%{search}%") | 
                Tool.description.ilike(f"%{search}%")
            )
        
        if active_only:
            query = query.filter(Tool.is_active == True)

        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    async def get_tool_by_id(
        db: Session,
        tool_id: int
    ) -> Optional[Tool]:
        tool = db.query(Tool).filter(Tool.id==tool_id).first()
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool with id-{tool_id} not found.")
        
        return tool
    
    @staticmethod
    async def create_tool(db: Session, tool_data: ToolCreate) -> Tool:
        db_tool = Tool(**tool_data.model_dump())
        db.add(db_tool)
        db.commit()
        db.refresh(db_tool)
        return db_tool

    @staticmethod
    async def update_tool(
        db: Session, 
        tool_id: int, 
        tool_data: ToolUpdate
    ) -> Tool:
        tool = await ToolService.get_tool_by_id(db, tool_id)
        
        update_data = tool_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(tool, field, value)
        
        db.commit()
        db.refresh(tool)
        return tool