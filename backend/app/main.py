from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

app = FastAPI(title="BECOME SELF API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    """Sunucu ayakta mı?"""
    return {"status": "ok"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)) -> dict:
    """Sunucu veritabanına ulaşabiliyor mu?"""
    db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
