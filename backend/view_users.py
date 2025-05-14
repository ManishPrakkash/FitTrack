from pymongo import MongoClient
import json
from bson import json_util

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fittrack_db']
users_collection = db['users']

# Get all users
users = list(users_collection.find())

# Convert MongoDB objects to JSON
def parse_json(data):
    return json.loads(json_util.dumps(data))

# Print users in a readable format
print("\n=== USERS IN MONGODB ===\n")
for user in users:
    # Convert MongoDB document to JSON
    user_json = parse_json(user)
    
    # Print user details
    print(f"ID: {user_json.get('id')}")
    print(f"Name: {user_json.get('name')}")
    print(f"Email: {user_json.get('email')}")
    print(f"Password (hashed): {user_json.get('password')}")
    print(f"Created At: {user_json.get('created_at')}")
    print(f"Updated At: {user_json.get('updated_at')}")
    print("-" * 50)

print(f"\nTotal Users: {len(users)}")
