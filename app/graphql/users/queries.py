import strawberry
from strawberry.types import Info
from sqlmodel import Session, select

from app.core.database import engine
from app.models.user import User
from app.graphql.users.types import UserGraphQLType


@strawberry.type
class UserQuery:

    @strawberry.field
    def users(self, info: Info) -> list[UserGraphQLType]:

        db = info.context["db"]
        users = db.exec(select(User)).all()
        return [
            UserGraphQLType(
                id=user.id,
                name=user.name,
                email=user.email,
                age=user.age,
                nickname=user.nickname,
            )
            for user in users
        ]

    @strawberry.field
    def user(self, info: Info, id: int) -> UserGraphQLType | None:

        db = info.context["db"]
        user = db.get(User, id)

        if user is None:
            return None

        return UserGraphQLType(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age,
            nickname=user.nickname,
        )