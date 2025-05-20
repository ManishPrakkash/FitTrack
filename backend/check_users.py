"""
Script to check users in MongoDB Atlas.
"""
import os
import sys
import django
import datetime
from pymongo import MongoClient
from bson import ObjectId
import json

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_backend.settings')
django.setup()

# MongoDB connection settings
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db')
DB_NAME = 'fittrack_db'

# Custom JSON encoder for MongoDB ObjectId and datetime
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def check_users():
    """Check users in MongoDB Atlas."""
    print("Checking users in MongoDB Atlas...")

    try:
        # Connect to MongoDB Atlas
        client = MongoClient(MONGODB_URI)
        db = client[DB_NAME]

        # Check users collection
        users_collection = db['users']
        users_count = users_collection.count_documents({})
        print(f"Found {users_count} users in the 'users' collection")

        # List all users
        if users_count > 0:
            print("\nUsers:")
            for user in users_collection.find():
                # Remove password for security
                if 'password' in user:
                    user['password'] = '********'
                print(json.dumps(user, cls=JSONEncoder, indent=2))

        # Check profiles collection
        profiles_collection = db['profiles']
        profiles_count = profiles_collection.count_documents({})
        print(f"\nFound {profiles_count} profiles in the 'profiles' collection")

        # List all profiles
        if profiles_count > 0:
            print("\nProfiles:")
            for profile in profiles_collection.find():
                print(json.dumps(profile, cls=JSONEncoder, indent=2))

        return True
    except Exception as e:
        print(f"Error checking users: {e}")
        return False

if __name__ == "__main__":
    success = check_users()
    sys.exit(0 if success else 1)
