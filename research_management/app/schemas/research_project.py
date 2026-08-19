from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

# Member Schemas
class ResearchMemberBase(BaseModel):
    role: Optional[str] = "MEMBER"

class ResearchMemberCreate(ResearchMemberBase):
    user_id: int

class ResearchMemberResponse(ResearchMemberBase):
    project_id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Project Schemas
class ResearchProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ResearchProjectCreate(ResearchProjectBase):
    pass

class ResearchProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ResearchProjectResponse(ResearchProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)