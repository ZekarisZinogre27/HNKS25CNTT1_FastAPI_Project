from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Literal, Optional

TaskStatus = Literal["TODO", "IN_PROGRESS", "DONE"]
TaskPriority = Literal["LOW", "MEDIUM", "HIGH"]

class ResearchTaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = "TODO"
    priority: TaskPriority = "MEDIUM"
    due_date: Optional[datetime] = None

class ResearchTaskCreate(ResearchTaskBase):
    assignee_id: Optional[int] = None

class ResearchTaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None

class ResearchTaskResponse(ResearchTaskBase):
    id: int
    project_id: int
    assignee_id: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)