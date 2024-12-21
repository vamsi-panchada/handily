from fastapi import APIRouter
from app.api.v1.endpoints import tools

api_router = APIRouter()
api_router.include_router(tools.router, tags=["tools"])