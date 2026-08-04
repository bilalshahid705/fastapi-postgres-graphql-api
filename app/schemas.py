from typing import Optional
from sqlmodel import SQLModel

# Fields required to create a new hero (No ID needed here)
class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

# Fields returned to the client (Ensures schema consistency)
class HeroRead(SQLModel):
    id: int
    name: str
    secret_name: str
    age: Optional[int] = None
