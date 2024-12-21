from fastapi import FastAPI
from .core.config import get_settings
from .core.database import get_db
from app.api.v1 import api_router


settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Toolbelt API"}