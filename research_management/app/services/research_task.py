from typing import Optional

from sqlalchemy import asc, case
from sqlalchemy.orm import Query, Session

from app.core.exceptions import ForbiddenException, NotFoundException
from app.models.research_project import ResearchProject
from app.models.research_task import ResearchTask
from app.models.user import User
from app.schemas.research_task import ResearchTaskCreate, ResearchTaskUpdate
from app.services.research_project import get_membership


def get_task_or_404(db: Session, task_id: int) -> ResearchTask:
    task = db.query(ResearchTask).filter(ResearchTask.id == task_id).first()
    if task is None:
        raise NotFoundException("Không tìm thấy nhiệm vụ nghiên cứu")
    return task


def require_project_member(db: Session, project_id: int, user: User) -> ResearchProject:
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()
    if project is None:
        raise NotFoundException("Không tìm thấy đề tài")
    if get_membership(db, project_id, user.id) is None:
        raise ForbiddenException("Bạn không phải thành viên của đề tài")
    return project


def require_assignee_member(db: Session, project_id: int, assignee_id: Optional[int]) -> None:
    if assignee_id is not None and get_membership(db, project_id, assignee_id) is None:
        raise ForbiddenException("Chỉ có thể giao nhiệm vụ cho thành viên của đề tài")


def create_task(
    db: Session, project_id: int, task_in: ResearchTaskCreate, user: User
) -> ResearchTask:
    require_project_member(db, project_id, user)
    require_assignee_member(db, project_id, task_in.assignee_id)
    task = ResearchTask(project_id=project_id, **task_in.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(
    db: Session,
    project_id: int,
    user: User,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee_id: Optional[int] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    sort: str = "due_date",
) -> list[ResearchTask]:
    require_project_member(db, project_id, user)
    query: Query[ResearchTask] = db.query(ResearchTask).filter(ResearchTask.project_id == project_id)
    if status:
        query = query.filter(ResearchTask.status == status)
    if priority:
        query = query.filter(ResearchTask.priority == priority)
    if assignee_id is not None:
        query = query.filter(ResearchTask.assignee_id == assignee_id)
    if search:
        query = query.filter(ResearchTask.title.ilike(f"%{search}%"))
    sort_column = ResearchTask.created_at if sort == "created_at" else ResearchTask.due_date
    nulls_last = case((sort_column.is_(None), 1), else_=0)
    query = query.order_by(nulls_last, asc(sort_column), ResearchTask.id)
    return query.offset((page - 1) * page_size).limit(page_size).all()


def get_task(db: Session, task_id: int, user: User) -> ResearchTask:
    task = get_task_or_404(db, task_id)
    require_project_member(db, task.project_id, user)
    return task


def update_task(
    db: Session, task_id: int, task_in: ResearchTaskUpdate, user: User
) -> ResearchTask:
    task = get_task_or_404(db, task_id)
    project = require_project_member(db, task.project_id, user)
    if user.id != project.owner_id and user.id != task.assignee_id:
        raise ForbiddenException("Chỉ OWNER hoặc người được giao mới có thể cập nhật nhiệm vụ")
    values = task_in.model_dump(include=task_in.model_fields_set)
    if "assignee_id" in values:
        require_assignee_member(db, task.project_id, values["assignee_id"])
    for field, value in values.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user: User) -> None:
    task = get_task_or_404(db, task_id)
    project = require_project_member(db, task.project_id, user)
    if user.id != project.owner_id:
        raise ForbiddenException("Chỉ OWNER mới có thể xóa nhiệm vụ")
    db.delete(task)
    db.commit()