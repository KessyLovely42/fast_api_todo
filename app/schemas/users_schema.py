from utils import Roles
from pydantic import BaseModel, Field

class CreateUser(BaseModel):
    email: str = Field(max_length=100, description="email address of the user")
    username: str = Field(max_length=100, description ="username of the user")
    first_name: str = Field(max_length =100, description = "first name of the user")
    last_name: str = Field(max_length =100, description = "first name of the user")
    hashed_password: str
    role: Roles

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    role: Roles
