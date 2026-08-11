import strawberry
from typing import Optional

@strawberry.type
class UserGraphQLType:
    id: int
    name: str
    email: str
    age: int | None
    nickname: str | None