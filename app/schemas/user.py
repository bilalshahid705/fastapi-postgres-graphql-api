from typing import Optional
from sqlmodel import SQLModel

class UserCreate(SQLModel):
    name: str
    email: str
    age: int
    nickname: Optional[str] = None

class UserRead(SQLModel):
    name: str
    email: str
    age: int
    nickname: Optional[str] = None
