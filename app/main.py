from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
# from app.core.logging_config import setup_logging

# logger = setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create required directories
    settings.UPLOAD_DIR.mkdir(exist_ok=True)
    
    # Include routers
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

app = create_app()