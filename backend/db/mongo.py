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
    if db is None:
        await connect_to_mongo()
    return db[collection_name]

async def insert_document(collection_name: str, model: BaseModel | dict):
    """Insert a Pydantic/SQLModel model or dictionary into MongoDB collection."""
    try:
        collection = await get_collection(collection_name)

        # Handle both Pydantic models and dictionaries
        if isinstance(model, BaseModel):
            document = model.model_dump(exclude_none=True, exclude={'id'})
        else:
            document = {k: v for k, v in model.items() if v is not None and k != 'id'}
            
        result = await collection.insert_one(document)
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting document into {collection_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to insert document into {collection_name}"
        )

async def find_one(collection_name: str, query: dict):
    """Find a single document in MongoDB collection."""
    try:
        collection = await get_collection(collection_name)
        document = await collection.find_one(query)
        if document:
            # Convert ObjectId to string in the returned document
            document["id"] = str(document["_id"])
            del document["_id"]
        return document
    except Exception as e:
        print(f"Error finding document in {collection_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find document in {collection_name}"
        )

async def find_many(collection_name: str, query: dict):
    """Find multiple documents in MongoDB collection."""
    try:
        collection = await get_collection(collection_name)
        documents = await collection.find(query).to_list(length=None)
        return documents
    except Exception as e:
        print(f"Error finding documents in {collection_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find documents in {collection_name}"
        )