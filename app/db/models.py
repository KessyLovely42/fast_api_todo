
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from random import randint

#import priority class from the schemas script
from utils import Priority, Roles

#import created base class from the 
from db.db_con import Base 
from typing import List, Optional, Union

from datetime import datetime

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

    

    #def __init__(self, username: str, first_name: str, last_name: str, )

class todos(Base):
    #table name
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]
    completed: Mapped[bool] 
    date_created: Mapped[str]
    priority: Mapped[Priority] #User object from the Priority class defined

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    #user: Mapped["User"] = relationship(back_populates="todos")

    # def __init__(self, title: str, description: Optional[str], completed : bool, priority: int):
    #     self.title = title
    #     self.description = description
    #     self.completed = completed 
    #     self.priority = priority 
    #     self.date_created = datetime.now()

    
