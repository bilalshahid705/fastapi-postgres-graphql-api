from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import text, Session
from strawberry.fastapi import GraphQLRouter
from app.graphql.graphql_schema import graphql_schema

from app.api import api_router
from app.core.config import settings
from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    with Session(engine) as session:
        session.exec(text("SELECT 1"))
    yield


async def get_context():
    with Session(engine) as session:
        yield {
            "db": session
        }


app = FastAPI(
    title="FastAPI E-commerce API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:8000", "https://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


graphql_app = GraphQLRouter(graphql_schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")
app.include_router(api_router, prefix="/api/v1")