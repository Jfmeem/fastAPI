from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import models
from typing import Annotated, Optional
from models import Todo
from database import engine, SessionLocal
from router import auth

app = FastAPI()

class Todos(BaseModel):
    id: int
    title: str
    description: str = Field(description="Maximum length is 100 characters", max_length=100)
    priority: int = Field(gt=0, lt=6, description="Priority must be between 1 and 5")
    completed: bool = False
    
class updateTodos(BaseModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None,description="Maximum length is 100 characters", max_length=100)
    priority: Optional[int] = Field(default=None,gt=0, lt=6, description="Priority must be between 1 and 5")
    completed: Optional[bool] = Field(default=None)

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)

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


@app.put('/edit/{todo_id}')
def update_todos(db: db_dependency, todo_id: int, updated_todo: updateTodos):
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="To do not found")
    
    update_data = updated_todo.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(todo, key, value)
        
    db.commit()
    
    return JSONResponse(status_code=200, content={"message": "To do updated successfully"})
    
     
     
@app.delete('/delete/{todo_id}')
def delete_todo(db: db_dependency, todo_id: int):
    
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="To do not found")

    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    
    return JSONResponse(status_code=200, content={"message": "To do deleted successfully"})