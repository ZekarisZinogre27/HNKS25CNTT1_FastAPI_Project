from fastapi import FastAPI, HTTPException
from app.core.exceptions import register_exception_handlers
from app.db.database import engine, Base
from app.models import research_project, research_task, users
from app.routers import auth, users as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

register_exception_handlers(app)

app.include_router(auth.router)
app.include_router(users_router.router)

@app.get("/migration")
def health_check():
    return {
        "status": "Code đang chạy",
        "message": "Research Group Management API đang chạy"
    }

@app.get("/")
def root():
    return {"message": "chào"}