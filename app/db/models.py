from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

#import priority class from the schemas script
from db.schemas import Priority 

#import created base class from the 
from db.db_con import Base 

class todos(Base):
    #table name
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]]
    completed: Mapped[bool] 
    date_created: Mapped[str]
    priority: Mapped[Priority] #User object from the Priority class defined
