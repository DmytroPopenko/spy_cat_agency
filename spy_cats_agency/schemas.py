
from pydantic import BaseModel, Field
from typing import List, Optional

class TargetBase(BaseModel):
    name: str
    country: str
    notes: str
    is_complete: bool = Field(default=False)

class TargetCreate(TargetBase):
    pass

class Target(TargetBase):
    id: int
    mission_id: int
    
    class Config:
        orm_mode = True

class MissionBase(BaseModel):
    is_complete: bool = Field(default=False)

class MissionCreate(MissionBase):
    targets: List[TargetCreate]

class Mission(MissionBase):
    id: int
    cat_id: int
    targets: List[Target] = Field(default_factory=list)
    
    class Config:
        orm_mode = True


class SpyCatBase(BaseModel):
    name: str
    experience_years: int
    breed: str
    salary: float

class SpyCatCreate(SpyCatBase):
    pass

class SpyCat(SpyCatBase):
    id: int
    mission: Optional[Mission] = None
    
    class Config:
        orm_mode = True
