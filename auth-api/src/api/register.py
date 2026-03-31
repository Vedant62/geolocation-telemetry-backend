from sqlalchemy import select
from fastapi import APIRouter, HTTPException
from api.models import UserCreate, UserResponse
from app.db import db_dependency, users
from app.utils import hash_password

router = APIRouter()

@router.post("/")
async def register_user(user: UserCreate, db: db_dependency):
    existing = await db.fetch_one(
        query=select(users).where(users.c.email == user.email)
    )
    if existing:
        raise HTTPException(status_code=409, detail='Email already in use')
    
    pwd = hash_password(user.password)
    query = users.insert().values(email=user.email, password=pwd).returning(users.c.id, users.c.email)
    row=await db.fetch_one(query)
    if not row:
        raise HTTPException(status_code=500, detail='Failed to create user')
    
    return UserResponse.model_validate(dict(row))



    
    




