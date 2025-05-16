from pymongo import MongoClient
import json
from bson import json_util

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fitrack_db']
users_collection = db['users']

# Count users
user_count = users_collection.count_documents({})
print(f"Number of users in database: {user_count}")

# Get all users
users = list(users_collection.find({}))

# Print users (without password)
print("\nUsers in database:")
for user in users:
    # Remove password for security
    if 'password' in user:
        user['password'] = '***HIDDEN***'
    
    # Convert MongoDB document to JSON
    user_json = json.loads(json_util.dumps(user))
    print(json.dumps(user_json, indent=2))
