from enum import IntEnum
from passlib.context import CryptContext
from sqlalchemy import select
from datetime import timedelta, timezone, datetime
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Annotated

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

#load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')



#Priority item
class Priority(IntEnum):
    """Helper class to define the priority of the to do item"""
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class Roles(IntEnum):
    ADMIN = 1
    USER = 2


def verify_user(username: str, password: str, db, model):
    stmt = select(model).where(model.username == username)
    user = db.scalars(stmt).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp":expires})
    token = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        print(f"in get_current_user access token is {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail="Userid or password not found")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is not valid")