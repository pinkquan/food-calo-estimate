from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from bson import ObjectId

class User(UserMixin):
    def __init__(self, username, email, password_hash, _id=None, created_at=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self._id = _id
        self.created_at = created_at or datetime.now()

    def get_id(self):
        return str(self._id)

    @staticmethod
    def get_by_id(user_id):
        from config.database import users
        user_data = users.find_one({"_id": user_id})
        if user_data:
            return User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=user_data["password_hash"],
                _id=user_data["_id"],
                created_at=user_data.get("created_at", datetime.now())
            )
        return None

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "created_at": self.created_at
        }

    def update_profile(self, username=None, new_password=None):
        from config.database import users
        update_data = {}
        
        if username:
            update_data["username"] = username
            self.username = username
            
        if new_password:
            password_hash = generate_password_hash(new_password)
            update_data["password_hash"] = password_hash
            self.password_hash = password_hash
            
        if update_data:
            users.update_one(
                {"_id": self._id},
                {"$set": update_data}
            )
            return True
        return False

class FoodRecord:
    def __init__(self, user_id, results, total_calories, created_at=None):
        self.user_id = user_id
        self.results = results
        self.total_calories = total_calories
        self.created_at = created_at or datetime.now()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "results": self.results,
            "total_calories": self.total_calories,
            "created_at": self.created_at
        }

    @staticmethod
    def get_by_user_id(user_id):
        from config.database import food_records
        records = food_records.find({"user_id": user_id}).sort("created_at", -1)
        return [FoodRecord(
            user_id=record["user_id"],
            results=record["results"],
            total_calories=record["total_calories"],
            created_at=record.get("created_at", datetime.now())
        ) for record in records]