from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.users import User
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user, require_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("", response_model=List[UserResponse])
def get_users(
    q: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    query = db.query(User)
    if q:
        query = query.filter((User.full_name.contains(q)) | (User.email.contains(q)))
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()