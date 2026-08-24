from app.db.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class ResearchProject(Base):
    __tablename__ = "research_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="owned_projects")
    members = relationship(
        "ResearchMember",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    tasks = relationship(
        "ResearchTask",
        back_populates="project",
        cascade="all, delete-orphan",
    )


class ResearchMember(Base):
    __tablename__ = "research_members"

    project_id = Column(Integer, ForeignKey("research_projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(50), nullable=False, default="MEMBER")
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    project = relationship("ResearchProject", back_populates="members")
    user = relationship("User", back_populates="project_memberships")