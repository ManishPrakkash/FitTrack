from pymongo import MongoClient
import sys

# Email to check
email_to_check = "manish@gmail.com"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fitrack_db']
users_collection = db['users']

# Check if user exists
user = users_collection.find_one({"email": email_to_check})

if user:
    print(f"User found with email: {email_to_check}")
    print(f"User name: {user.get('name')}")
    print(f"User ID: {user.get('id')}")
else:
    print(f"No user found with email: {email_to_check}")
    
    # Check for case sensitivity issues
    case_insensitive_query = {"email": {"$regex": f"^{email_to_check}$", "$options": "i"}}
    case_insensitive_user = users_collection.find_one(case_insensitive_query)
    
    if case_insensitive_user:
        print(f"Found user with case-insensitive match: {case_insensitive_user.get('email')}")
    
    # List all emails for reference
    print("\nAll emails in database:")
    all_users = users_collection.find({}, {"email": 1})
    for u in all_users:
        print(f"- {u.get('email')}")
