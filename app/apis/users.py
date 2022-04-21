from locale import currency
from typing import List
from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from . import models, schemas, oauth2
from ..database import get_db
from ..utils.helper import Helper

userAPI = APIRouter(tags=["Users"])

@userAPI.get("/")
def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return {"users":all_users}

@userAPI.get("/{id}", response_model=schemas.ResponseUser)
def get_a_user(id: int, db: Session = Depends(get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find {id} resource")
    return user

@userAPI.post("/", status_code=status.HTTP_201_CREATED)
def create_a_user(new_user: schemas.User, db: Session = Depends(get_db)):
    new_user.password = Helper.encrypt_password(new_user.password)
    new_usr = models.User(**new_user.dict())
    db.add(new_usr)
    db.commit()
    db.refresh(new_usr)
    return {"message": "User Created"}


@userAPI.put("/{id}")
def update_a_user(id: int, updated_user: schemas.User, db: Session = Depends(get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id == id)

    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find {id} resource")
    updated_user.password = Helper.encrypt_password(updated_user.password)
    user_query.update(updated_user.dict(),synchronize_session=False)
    db.commit()
    return {"message": "User Updated"}

@userAPI.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_a_user(id: int, db: Session = Depends(get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unable to find {id} resource")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@userAPI.post("/login",status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login_a_user(auth_user: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == auth_user.username)
    user = user_query.first()
    if user ==None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    if Helper.verify_password(auth_user.password,user.password)==False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
    access_token = oauth2.create_token(data = {"username":auth_user.username})
    return {"message":"Authenticated", "access_token":access_token, "token_type": "bearer" }

@userAPI.post("/auth",status_code=status.HTTP_200_OK, response_model=schemas.ResponseUser)
def authenticate_a_user(db: Session = Depends(get_db), user: schemas.User = Depends(oauth2.get_current_user)):
    print(f"Authenticated - {user.email}")
    return user