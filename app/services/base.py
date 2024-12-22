from abc import ABC, abstractmethod
from typing import Any, Dict
from pathlib import Path

class BaseToolService(ABC):
    """Base class for all tool services"""
    
    @abstractmethod
    async def process(self, file_path: Path, **kwargs) -> Dict[str, Any]:
        """Process the input and return results"""
        pass
    
    @abstractmethod
    async def validate_input(self, file_path: Path, **kwargs) -> bool:
        """Validate the input before processing"""
        pass