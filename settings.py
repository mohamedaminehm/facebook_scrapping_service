from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import motor.motor_asyncio
import asyncio



MONGO_DETAILS = "mongodb://root:root@mongo_db:27017"


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
client.get_io_loop = asyncio.get_event_loop
db = client.app_db
# db: motor.motor_asyncio.AsyncIOMotorDatabase = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)["app_db"]

def get_db() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return db


# student_collection = db.get_collection("students_collection")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)