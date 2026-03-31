from contextlib import asynccontextmanager
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from api import location
import json
from app import producer
from shared.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    producer.kafka_producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_server_url,
        value_serializer= lambda v: json.dumps(v).encode('utf-8')
    )

    await producer.kafka_producer.start()
    print("Kafka producer started")

    yield

    await producer.kafka_producer.stop()
    print("Kafka producer stopped")

app = FastAPI(lifespan=lifespan)
app.include_router(location.router, prefix="/location")
