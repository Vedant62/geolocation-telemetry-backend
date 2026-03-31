from sqlalchemy import MetaData, Table, Column, Integer, String
from shared.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from databases import Database
from typing import Annotated
from fastapi import Depends

metadata = MetaData()
async_engine = create_async_engine(settings.database_url)
database = Database(settings.database_url)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(50), index=True),
    Column("password", String(255))
)

async def get_db():
    yield database
db_dependency = Annotated[Database, Depends(get_db)]