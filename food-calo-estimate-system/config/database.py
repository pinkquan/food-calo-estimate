from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load biến môi trường từ .env
load_dotenv()

# Lấy thông tin kết nối từ biến môi trường
MONGO_URI = os.getenv('MONGO_URI', '')  # Fallback nếu không có trong .env
DB_NAME = os.getenv('DB_NAME', '')  # Fallback nếu không có trong .env

try:
    # Kết nối tới MongoDB với URI từ biến môi trường
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]

    # Tạo/truy cập collections
    users = db.users
    food_records = db.food_records
    
    # Tạo unique index cho email trong collection users
    users.create_index("email", unique=True)
    
    print(f"Connected to MongoDB database: {DB_NAME} successfully!")

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise e