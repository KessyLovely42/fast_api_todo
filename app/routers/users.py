from fastapi import APIRouter, HTTPException
from utils import UserDep
from db.db_con import SessionDep
from db.models import User
from schemas.users_schema import PasswordRequest
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags = ["users"]
)

pass_encrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/")
async def show_user_info(user: UserDep, session: SessionDep):
    user_db = session.get(User, user.get("id"))

    if not user_db:
        raise HTTPException(status_code=404, detail="user not found")
    return user_db

@router.patch("/change-password")
async def change_password(user: UserDep, 
                          password: PasswordRequest, 
                          session: SessionDep):
    if user is None:
        raise HTTPException(status_code=404, detail="Not autorized")

    if not password:
        return "password cannot be empty"
    old_password = password.old_password
    new_password = password.new_password

    user_db = session.get(User, user.get("id"))
    if pass_encrypt.verify(old_password, user_db.hashed_password):
        user_db.hashed_password = pass_encrypt.hash(new_password)
        session.commit()
        return "password change successful"
    
    else:
        return "password does not match"