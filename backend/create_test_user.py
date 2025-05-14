from pymongo import MongoClient
from django.contrib.auth.hashers import make_password
import uuid
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fittrack_backend.settings")
django.setup()

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['fitrack_db']
users_collection = db['users']

# Check if user already exists
existing_user = users_collection.find_one({'email': 'test@example.com'})
if existing_user:
    print("User already exists:", existing_user['id'])
else:
    # Create user document
    user = {
        'id': str(uuid.uuid4()),
        'name': 'Test User',
        'email': 'test@example.com',
        'password': make_password('password123'),
        'created_at': None,
        'updated_at': None
    }
    
    # Insert user into MongoDB
    result = users_collection.insert_one(user)
    
    if result.inserted_id:
        print("User created successfully with ID:", user['id'])
    else:
        print("Failed to create user")

# List all users
print("\nAll users in database:")
for user in users_collection.find():
    print(f"- {user['name']} ({user['email']})")
