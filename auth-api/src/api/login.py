from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from api.models import Token
from api.models import UserCreate
from app.db import db_dependency, users
from app.utils import create_access_token, verify_password

router = APIRouter()

@router.post("/", response_model=Token)
async def login(user: UserCreate, db: db_dependency):
    query = select(users).where(users.c.email == user.email)
    row = await db.fetch_one(query)

    if not row:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    flag = verify_password(user.password, row["password"])
    if not flag:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub":str(row["id"])})
    return Token(access_token=access_token)