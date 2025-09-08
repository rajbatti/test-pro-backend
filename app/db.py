from motor.motor_asyncio import AsyncIOMotorClient
from app import config

client = AsyncIOMotorClient(config.MONGO_URI)
db = client[config.DB_NAME]

questions_collection = db["questions"]
