from mongoengine import Document, StringField, DateTimeField, BooleanField
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import users_collection

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(default='user', choices=['user', 'admin'])
    api_key = StringField(unique=True, sparse=True)
    api_key_expires_at = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    is_active = BooleanField(default=True)

    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'username',
            'api_key'
        ]
    }

    def __init__(self, **data):
        super(User, self).__init__(**data)
        self.password_hash = generate_password_hash(self.password)

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @staticmethod
    def from_dict(data):
        user = User(
            username=data["username"],
            email=data["email"],
            password="",  # Password will be set separately
            role=data.get("role", "user")
        )
        user.password_hash = data["password_hash"]
        user.created_at = data["created_at"]
        user.updated_at = data["updated_at"]
        return user

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def find_by_email(email):
        user_data = users_collection.find_one({"email": email})
        if user_data:
            return User.from_dict(user_data)
        return None

    @staticmethod
    def find_by_username(username):
        user_data = users_collection.find_one({"username": username})
        if user_data:
            return User.from_dict(user_data)
        return None

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super(User, self).save(*args, **kwargs) 