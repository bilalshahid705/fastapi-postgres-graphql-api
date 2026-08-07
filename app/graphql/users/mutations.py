import strawberry
from strawberry.types import Info

from sqlmodel import Session

from app.models.user import User
from app.graphql.users.types import UserGraphQLType


@strawberry.type
class UserMutation:

    @strawberry.mutation
    def create_user(
        self,
        info: Info,
        name: str,
        email: str,
        age: int | None = None,
        nickname: str | None = None,
    ) -> UserGraphQLType:

        db: Session = info.context["db"]

        user = User(
            name=name,
            email=email,
            age=age,
            nickname=nickname,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return UserGraphQLType(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age,
            nickname=user.nickname,
        )

    @strawberry.mutation
    def update_user(
        self,
        info: Info,
        id: int,
        name: str | None = None,
        email: str | None = None,
        age: int | None = None,
        nickname: str | None = None,
    ) -> UserGraphQLType | None:

        db: Session = info.context["db"]

        user = db.get(User, id)

        if user is None:
            return None

        if name is not None:
            user.name = name

        if email is not None:
            user.email = email

        if age is not None:
            user.age = age

        if nickname is not None:
            user.nickname = nickname

        db.add(user)
        db.commit()
        db.refresh(user)

        return UserGraphQLType(
            id=user.id,
            name=user.name,
            email=user.email,
            age=user.age,
            nickname=user.nickname,
        )

    @strawberry.mutation
    def delete_user(
        self,
        info: Info,
        id: int,
    ) -> bool:

        db: Session = info.context["db"]

        user = db.get(User, id)

        if user is None:
            return False

        db.delete(user)
        db.commit()

        return True