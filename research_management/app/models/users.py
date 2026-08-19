from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="USER", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)

    owned_projects = relationship("ResearchProject", back_populates="owner")
    project_memberships = relationship("ResearchMember", back_populates="user")
    assigned_tasks = relationship("ResearchTask", back_populates="assignee")