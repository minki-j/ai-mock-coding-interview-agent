import os
from pymongo import MongoClient
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel

# MongoDB connection configuration
MONGO_URL = os.getenv("MONGO_URL", "")
print(f"==>> MONGO_URL: {MONGO_URL}")
DB_NAME = "main"

# Initialize MongoDB client
client: Optional[MongoClient] = None
db = None

def connect_to_mongo():
    """Connect to MongoDB and initialize database client."""
    global client, db
    try:
        client = MongoClient(
            MONGO_URL,
            tls=True,
            tlsAllowInvalidCertificates=False,
            serverSelectionTimeoutMS=5000
        )
        db = client[DB_NAME]
        # Verify connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

def close_mongo_connection():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")

def get_collection(collection_name: str):
    """Get MongoDB collection by name."""
    if db is None:
        connect_to_mongo()
    return db[collection_name]

def insert_document(collection_name: str, model: BaseModel | dict):
    """Insert a Pydantic/SQLModel model or dictionary into MongoDB collection."""
    try:
        collection = get_collection(collection_name)

        # Handle both Pydantic models and dictionaries
        if isinstance(model, BaseModel):
            document = model.model_dump(exclude_none=True, exclude={'id'})
        else:
            document = {k: v for k, v in model.items() if v is not None and k != 'id'}
            
        result = collection.insert_one(document)
        return result.inserted_id
    except Exception as e:
        print(f"Error inserting document into {collection_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to insert document into {collection_name}"
        )

def find_one(collection_name: str, query: dict):
    """Find a single document in MongoDB collection."""
    try:
        collection = get_collection(collection_name)
        document = collection.find_one(query)
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

def find_many(collection_name: str, query: dict):
    """Find multiple documents in MongoDB collection."""
    try:
        collection = get_collection(collection_name)
        documents = list(collection.find(query))
        # Convert ObjectIds to strings
        for doc in documents:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
        return documents
    except Exception as e:
        print(f"Error finding documents in {collection_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find documents in {collection_name}"
        )
    
def delete_many(collection_name: str, query: dict):
    """Delete multiple documents in MongoDB collection."""
    try:
        collection = get_collection(collection_name)
        collection.delete_many(query)
    except Exception as e:
        print(f"Error deleting documents in {collection_name}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to delete documents in {collection_name}"
        )