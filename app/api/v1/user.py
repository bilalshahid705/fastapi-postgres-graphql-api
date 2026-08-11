from typing import List
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from app.core.database import get_db, engine
from app.models import User
from app.schemas import UserCreate, UserRead
from app.graphql.graphql_schema import graphql_schema
from app.core.cache import get_cache, set_cache

router = APIRouter(tags=["Users"])

@router.post("/users/", response_model=UserRead)
def create_user(user_in: UserCreate, session: Session = Depends(get_db)):
    
    db_user = User.model_validate(user_in)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@router.get("/users/", response_model=List[UserRead])
async def read_users(session: Session = Depends(get_db)):
    cache_key = "users:all"

    cached_users = await get_cache(cache_key)

    if cached_users is not None:
        return cached_users

    users = session.exec(select(User)).all()
    await set_cache(cache_key, users, expire=600)
    return users


@router.get("/graphql/users", response_model=List[UserRead])
async def get_users():
    query = """
    query {
        users {
            id
            name
            email
            age
            nickname
        }
    }
    """

    result = await graphql_schema.execute(
        query,
        context_value={
            "db": Session(engine)
        },
    )
    if result.errors:
        raise Exception(result.errors)

    return result.data["users"]


@router.get(
    "/graphql/users/{user_id}",
    response_model=UserRead,
)
async def get_user(user_id: int):

    query = """
    query GetUser($user_id: Int!) {
        user(id: $user_id) {
            id
            name
            email
            age
            nickname
        }
    }
    """

    with Session(engine) as db:
        result = await graphql_schema.execute(
            query,
            variable_values={
                "user_id": user_id,
            },
            context_value={
                "db": db,
            },
        )

    if result.errors:
        raise HTTPException(
            status_code=500,
            detail=str(result.errors),
        )

    return result.data["user"]


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_db)
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()

    return {"message": "User deleted successfully"}


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_in: UserCreate,
    session: Session = Depends(get_db)
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_in.model_dump()

    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user