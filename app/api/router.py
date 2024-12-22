from fastapi import APIRouter
from app.api.endpoints import pdf_tools, health

api_router = APIRouter()

# Register tool routers
api_router.include_router(
    pdf_tools.router,
    prefix="/pdf-tools",
    tags=["pdf-tools"]
)

api_router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)