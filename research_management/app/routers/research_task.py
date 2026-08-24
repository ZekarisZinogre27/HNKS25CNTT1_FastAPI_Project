from typing import List, Literal, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.research_task import (ResearchTaskCreate, ResearchTaskResponse, ResearchTaskUpdate, TaskPriority, TaskStatus)
from app.services import research_task as task_service

router = APIRouter(tags=["Research Tasks"])


@router.post("/research-projects/{project_id}/research-tasks", response_model=ResearchTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: int,
    task_in: ResearchTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(db, project_id, task_in, current_user)


@router.get("/research-projects/{project_id}/research-tasks", response_model=List[ResearchTaskResponse])
def list_tasks(
    project_id: int,
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    priority: Optional[TaskPriority] = None,
    assignee_id: Optional[int] = Query(None, alias="assignee"),
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: Literal["due_date", "created_at"] = "due_date",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.list_tasks(
        db, project_id, current_user, status_filter, priority, assignee_id,
        search, page, page_size, sort
    )


@router.get("/research-tasks/{task_id}", response_model=ResearchTaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.get_task(db, task_id, current_user)


@router.patch("/research-tasks/{task_id}", response_model=ResearchTaskResponse)
def update_task(
    task_id: int,
    task_in: ResearchTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.update_task(db, task_id, task_in, current_user)


@router.delete("/research-tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service.delete_task(db, task_id, current_user)
