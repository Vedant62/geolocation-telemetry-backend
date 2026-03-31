from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import async_engine, metadata, database
from api import login, register

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    await database.connect()

    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(register.router, prefix="/register")
app.include_router(login.router, prefix="/login")

