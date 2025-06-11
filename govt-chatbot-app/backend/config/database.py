from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB connection string from environment variable
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'govt_schemes_db')

# Create MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
schemes_collection = db.schemes
users_collection = db.users
chat_history_collection = db.chat_history 