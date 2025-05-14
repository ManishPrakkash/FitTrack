from pymongo import MongoClient
import json
from bson import json_util

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Check if fittrack_db exists
all_dbs = client.list_database_names()
print(f"All databases: {all_dbs}")

if 'fittrack_db' in all_dbs:
    print("\nfittrack_db exists!")

    # Get the fittrack_db database
    db = client['fittrack_db']

    # List all collections
    collections = db.list_collection_names()
    print(f"Collections in fittrack_db: {collections}")

    # Check if users collection exists
    if 'users' in collections:
        print("\nusers collection exists!")

        # Count documents in users collection
        count = db.users.count_documents({})
        print(f"Number of documents in users collection: {count}")

        # Print first user if any exist
        if count > 0:
            first_user = db.users.find_one()
            print("\nSample user document:")
            # Convert MongoDB document to JSON-compatible format
            user_json = json_util.loads(json_util.dumps(first_user))
            # Print key-value pairs
            for key, value in user_json.items():
                print(f"  {key}: {value}")
    else:
        print("\nusers collection does not exist!")

        # Create users collection with a test document
        print("Creating users collection with a test document...")
        result = db.users.insert_one({
            "name": "Test User",
            "email": "test_user@example.com",
            "password": "hashed_password"
        })
        print(f"Created test user with ID: {result.inserted_id}")
else:
    print("\nfittrack_db does not exist!")

    # Create fittrack_db and users collection
    print("Creating fittrack_db and users collection...")
    db = client['fittrack_db']
    result = db.users.insert_one({
        "name": "Test User",
        "email": "test_user@example.com",
        "password": "hashed_password"
    })
    print(f"Created test user with ID: {result.inserted_id}")

print("\nCheck complete.")
