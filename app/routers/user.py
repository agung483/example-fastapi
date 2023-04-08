from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/",response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.User).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the passord - user.password
    temp_user = db.query(models.User).filter(models.User.username == user.username).first()
    if temp_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {user.username} has already been taken by other")
    hashed_password = utils.hash(user.password) 
    user.password = hashed_password   
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} was not found")

    return user