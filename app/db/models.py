
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from random import randint

#import priority class from the schemas script
from utils import Priority, Roles

#import created base class from the 
from db.db_con import Base 
from typing import List, Optional, Union


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index = True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str] = mapped_column(unique= True)
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[Roles] 
    date_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    

    def __init__(self, 
                 email: str, 
                 username: str, 
                 first_name: str, 
                 last_name: str, 
                 hashed_password: str, 
                 is_active:bool, 
                 role: Roles):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.role = role

class todos(Base):
    #table name
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]
    completed: Mapped[bool] 
    date_created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    priority: Mapped[Priority] #User object from the Priority class defined

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    #user: Mapped["User"] = relationship(back_populates="todos")

    def __init__(self, title: str, description: Optional[str], completed : bool, priority: int, user_id:str):
        self.title = title
        self.description = description
        self.completed = completed 
        self.priority = priority 
        self.user_id = user_id
    
    def to_dict(self) -> dict : 
        dict_obj = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "date_created": self.date_created,
            "priority":self.priority,
            "user_id": self.user_id

        }
        return dict_obj

    
