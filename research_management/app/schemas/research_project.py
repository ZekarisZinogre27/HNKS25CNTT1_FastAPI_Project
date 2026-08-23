from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class MemberAdd(BaseModel):
    user_id: int

class MemberResponse(BaseModel):
    project_id: int
    user_id: int
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResearchProjectBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None

class ResearchProjectCreate(ResearchProjectBase):
    pass

class ResearchProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None

class ProjectResponse(ResearchProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


ResearchMemberCreate = MemberAdd
ResearchMemberResponse = MemberResponse
ResearchProjectResponse = ProjectResponse