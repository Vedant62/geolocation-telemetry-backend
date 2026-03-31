from fastapi import APIRouter
from api.models import Location
from app.utils import auth_dependency

router = APIRouter()

@router.get("/ping")
async def pong():
    return {"msg": "pong"}

@router.post("/send")
async def get_location(location: Location, payload: auth_dependency):
    print(f"Location got: {{ {location.lat}, {location.lon} }} \nPayload: {payload}");