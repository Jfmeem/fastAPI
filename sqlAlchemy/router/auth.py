from fastapi import FastAPI, APIRouter, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from models import User
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUser(BaseModel):
    username : str
    email : str
    firstname : str
    lastname : str
    password : str
    role : str
    
def authenticate_user(username, password, db):
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        return False
    
    if bcrypt_context.verify(password, user.hash_password):
        return True
    
    return False
    
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

@router.post('/login')
def login_user(db : db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    authenticated = authenticate_user(form_data.username, form_data.password, db)
    if authenticated == True:
        return JSONResponse(status_code=200, content={"message": "Login successful"})
    else:
        return JSONResponse(status_code=401, content={"message": "Invalid username or password"})
    