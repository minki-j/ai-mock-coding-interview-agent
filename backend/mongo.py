import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel

# MongoDB connection configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "letscode"

# Initialize MongoDB client
client: Optional[AsyncIOMotorClient] = None
db = None

async def connect_to_mongo():
    """Connect to MongoDB and initialize database client."""
    global client, db
    try:
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        await client.admin.command('ping')  # Verify connection
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

async def get_collection(collection_name: str):
    """Get MongoDB collection by name."""
    if not db:
        await connect_to_mongo()
    return db[collection_name]

async def insert_document(collection_name: str, model: BaseModel):
    """Insert a Pydantic/SQLModel model into MongoDB collection."""
    try:
        collection = await get_collection(collection_name)
        # Convert model to dict, excluding None values
        document = model.model_dump(exclude_none=True, exclude={'id'})  # exclude id since MongoDB will generate _id
        result = await collection.insert_one(document)
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting document into {collection_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to insert document into {collection_name}"
        )
