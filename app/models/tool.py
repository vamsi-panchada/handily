from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from .base import TimeStampedBase
import enum

class ToolCategory(str, enum.Enum):
    CONVERTER = "converter"
    CALCULATOR = "calculator"
    FORMATTER = "formatter"
    VALIDATOR = "validator"
    GENERATOR = "generator"

class Tool(TimeStampedBase):
    __tablename__="tools"

    name = Column(String, index=True)
    description = Column(String)
    category = Column(SQLEnum(ToolCategory))
    icon = Column(String)
    is_active = Column(Boolean, default=True)
    endpoint = Column(String, unique=True)