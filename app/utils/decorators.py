import functools
from app.core.exceptions import ToolException
import logging

logger = logging.getLogger(__name__)

def handle_tool_errors(func):
    """Decorator to handle tool-specific errors"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ToolException as e:
            logger.error(f"Tool error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise ToolException(detail=str(e), status_code=500)
    return wrapper