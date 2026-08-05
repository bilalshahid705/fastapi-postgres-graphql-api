from typing import Optional
from sqlmodel import SQLModel, Field

class Villan(SQLModel, table=True):
    __tablename__ = "villans"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    