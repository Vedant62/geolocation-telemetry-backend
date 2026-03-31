from fastapi import FastAPI
from api import location
app = FastAPI()

app.include_router(location.router, prefix="/location")
