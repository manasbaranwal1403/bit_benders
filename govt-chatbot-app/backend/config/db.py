import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "govt_schemes_db")

# Create MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_db():
    return db
