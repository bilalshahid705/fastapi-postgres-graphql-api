from typing import List
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import Session, select
from app.core.database import get_db, engine
from app.models import User
from app.schemas import UserCreate, UserRead

router = APIRouter(tags=["Users"])

@router.post("/users/", response_model=UserRead)
def create_user(user_in: UserCreate, session: Session = Depends(get_db)):
    
    db_user = User.model_validate(user_in)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@router.get("/users/", response_model=List[UserRead])
def read_users(session: Session = Depends(get_db)):
    users = session.exec(select(User)).all()
    return users


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