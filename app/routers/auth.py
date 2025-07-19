from typing import Annotated, List
from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from db.models import User
from schemas.users_schema import CreateUser, UserResponse

from passlib.context import CryptContext
from db.db_con import SessionDep

from utils import verify_user, create_token

from sqlalchemy import select

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

@router.get("/",status_code= status.HTTP_200_OK, 
            response_model=List[UserResponse])
async def get_users(session: SessionDep):
    
    stmt = select(User)
    users = session.scalars(stmt).all()
    
    return users

@router.post("/new-user/", status_code=status.HTTP_201_CREATED)
async def new_user(user: CreateUser, session: SessionDep):
    if not user:
        HTTPException(status_code=404, detail="Please enter a valid user")
    
    new_user = User(
        email = user.email,
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        hashed_password = bcrypt_context.hash(user.hashed_password),
        is_active = True,
        role = user.role
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@router.post("/token/")
async def login_for_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                          session: SessionDep): 
    user = verify_user(form_data.username, form_data.password, session, User)
    if not user:
        raise HTTPException(status_code=401, detail="Could not authorize user")
    access_token =  create_token(user.username, user.id, timedelta(minutes=10))
    print(f"in auth_user access token is {access_token}")
    return access_token
    # stmt = select(User).where(User.username == form_data.username)
    # user = session.scalars(stmt).first()
    # if not user:
    #     return "user does not exist"
    
    # if not bcrypt_context.verify(form_data.password, user.hashed_password):
    #     return "user not verified"
    #     #HTTPException(status_code=402, detail ="user cannot be verified")
    # return "user verified"
    
    

