from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel, ConfigDict

class DbBase(DeclarativeBase):
    pass

class PydanticBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
