from fastapi import FastAPI, HTTPException
from app.core.exceptions import register_exception_handlers
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

register_exception_handlers(app)

@app.get("/migration")
def health_check():
    return {
        "status": "Code đang chạy",
        "message": "Research Group Management API đang chạy"
    }

@app.get("/")
def root():
    return {"message": "chào"}