from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from api.models import Location
from app.utils import auth_dependency
from app.producer import get_producer

router = APIRouter()

@router.get("/ping")
async def pong():
    return {"msg": "pong"}

@router.post("/send")
async def get_location(location: Location, payload: auth_dependency, producer : AIOKafkaProducer = Depends(get_producer)):
    print(f"Location got: {{ {location.lat}, {location.lon} }} \nPayload: {payload}");

    event = {
        "user_id" : payload.get("sub"),
        "lat":location.lat,
        "lon":location.lon
    }

    await producer.send("driver_locations", value=event)
    return {"status": "success", "message": "Location queued for processing"}