from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUser(BaseModel):
    username : str
    email : str
    firstname : str
    lastname : str
    password : str
    role : str
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post('/createUser')
def create_user(db : db_dependency, new_user: CreateUser):
    model_user = User(
        username=new_user.username,
        email=new_user.email,
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        hash_password=bcrypt_context.hash(new_user.password),
        is_active=True,
        role=new_user.role
    )
    db.add(model_user)
    db.commit()
    
    return JSONResponse(status_code=201, content={"message": "User created successfully"})
