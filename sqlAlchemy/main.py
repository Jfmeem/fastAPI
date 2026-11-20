from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import models
from typing import Annotated
from models import Todo
from database import engine, SessionLocal

app = FastAPI()

class Todos(BaseModel):
    id: int
    title: str
    description: str = Field(description="Maximum length is 100 characters", max_length=100)
    priority: int = Field(gt=0, lt=6, description="Priority must be between 1 and 5")
    completed: bool = False

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
    
    
@app.post('/create/')
def create_todo(db: db_dependency, new_todo: Todos):
    model_todo = Todo(**new_todo.model_dump())
    db.add(model_todo)
    db.commit()
    
    return JSONResponse(status_code=201, content={"message": "To do created successfully"})