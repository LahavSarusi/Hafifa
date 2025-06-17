from typing import List, Optional
from pydantic import BaseModel, validator, Field
from datetime import datetime


class HeroSchema(BaseModel):
    id: Optional[int] = Field(default=None, alias='id')
    name: str = Field(..., alias='name')
    suit_color: str = Field(..., alias='suit_color')
    has_cape: bool = Field(..., alias='has_cape')
    last_mission: datetime = Field(..., alias='last_mission')
    is_retired: bool = Field(..., alias='is_retired')

    class Config:
        from_attributes = True


class NewHero(HeroSchema):
    powers: List[str]


class HeroFilters(BaseModel):
    name: str = None
    suit_color: str = None
    has_cape: bool = None

    @validator('has_cape', pre=True)
    def parse_has_cape(cls, v):
        if isinstance(v, bool) or v is None:
            return v
        if v.lower() == 'true':
            return True
        return False
