from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_db, engine  # Ensure engine is imported to log SQL queries
from app.models import Hero
from app.schemas import HeroCreate, HeroRead

app = FastAPI(title="FastAPI")

@app.post("/heroes/", response_model=HeroRead)
def create_hero(hero_in: HeroCreate, session: Session = Depends(get_db)):
    # logfire.info("Creating a new hero: {name}", name=hero_in.name)
    
    db_hero = Hero.model_validate(hero_in)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    
    return db_hero

@app.get("/heroes/", response_model=List[HeroRead])
def read_heroes(session: Session = Depends(get_db)):
    heroes = session.exec(select(Hero)).all()
    return heroes


@app.put("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(
    hero_id: int,
    hero_in: HeroCreate,
    session: Session = Depends(get_db)
):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero_in.model_dump()

    for key, value in hero_data.items():
        setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)

    return hero



@app.delete("/heroes/{hero_id}")
def delete_hero(
    hero_id: int,
    session: Session = Depends(get_db)
):
    hero = session.get(Hero, hero_id)

    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    session.delete(hero)
    session.commit()

    return {"message": "Hero deleted successfully"}