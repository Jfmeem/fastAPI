from fastapi import FastAPI, Depends, HTTPException
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


@app.get('/todos/{todo_id}')
def read_specific_todos(db: db_dependency, todo_id: int):
    specific_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if specific_todo is not None:
        return specific_todo
    else:
        raise HTTPException(status_code=404, detail="To do not found")