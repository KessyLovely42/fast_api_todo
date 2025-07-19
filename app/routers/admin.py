from fastapi import APIRouter, HTTPException
from db.db_con import SessionDep
from sqlalchemy import select
from db.models import User
from utils import verify_user, create_token, UserDep

router = APIRouter(
    prefix="/admin",
    tags = ["admin"]
)

@router.get("/")
async def get_users(session: SessionDep, user: UserDep):
    if user.get("role") == 1:
        stmt = select(User)
        users = session.scalars(stmt).all()
        return users
    
    raise HTTPException(status_code=401, detail="User not authorized")
    
