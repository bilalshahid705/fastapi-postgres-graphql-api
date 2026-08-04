from typing import Optional
from sqlmodel import SQLModel, Field

class Hero(SQLModel, table=True):
    __tablename__ = "heroes"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
