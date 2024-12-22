from fastapi import APIRouter, File, UploadFile
from typing import List
from app.models.base import ToolResponse
from app.services.tool_services.pdf_services import PDFService
from app.utils.file_handlers import save_upload_file, cleanup_file
from app.utils.decorators import handle_tool_errors
from app.core.config import settings

router = APIRouter()
pdf_service = PDFService()

@router.post("/pdf-to-latex")
@handle_tool_errors
async def convert_pdf_to_latex(file: UploadFile = File(...)) -> ToolResponse:
    """Convert a single PDF file to LaTeX format"""
    file_path = await save_upload_file(
        file,
        allowed_extensions=settings.TOOL_CONFIGS["pdf_tools"]["allowed_extensions"]
    )
    
    try:
        result = await pdf_service.process(file_path)
        return ToolResponse(
            success=True,
            message="Conversion successful",
            data=result
        )
    finally:
        cleanup_file(file_path)