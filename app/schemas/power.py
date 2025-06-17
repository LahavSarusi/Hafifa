from typing import Optional
from pydantic import BaseModel, Field


class PowerSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str = Field(..., alias='name')
    hero_id: int = Field(..., alias='hero_id')

    class Config:
        from_attributes = True
