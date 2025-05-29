from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', '')  
DB_NAME = os.getenv('DB_NAME', '') 

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    users = db.users
    food_records = db.food_records
    
    users.create_index("email", unique=True)
    
    print(f"Connected to MongoDB database: {DB_NAME} successfully!")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise e