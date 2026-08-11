from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True, index=True)
    age: Optional[int] = Field(default=None, index=True)
    nickname: Optional[str] = Field(default=None, nullable=True)