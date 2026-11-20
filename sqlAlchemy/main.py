from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from typing import Annotated
from models import Todo
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
        
@app.get('/')
def read_todos(db: db_dependency):
    return db.query(Todo).all()
    