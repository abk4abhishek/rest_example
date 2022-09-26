from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from . import schemas, models
from ..database import get_db
from ..config import settings

# SECRET_KEY
SECRET_KEY = settings.APP_AUTH_TOKEN_SECRET_KEY
ALGORITHM = settings.APP_AUTH_TOKEN_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.APP_AUTH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer("login")


def create_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("username")
        if username == None:
            raise credentials_exceptions
        token_data = schemas.TokenData(username=username)
    except JWTError as e:
        raise credentials_exceptions
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Unable to validate credentials",
                                           headers={"www-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exceptions)
    user = db.query(models.User).filter(models.User.email == token_data.username).first()
    return user
