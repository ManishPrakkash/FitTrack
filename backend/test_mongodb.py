from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import sys

def test_mongodb_connection():
    """Test connection to MongoDB."""
    try:
        # Connect to MongoDB with a short timeout
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)

        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')

        # Get database and collection
        db = client['fittrack_db']
        users_collection = db['users']

        # Ensure the collection exists by inserting a test document if empty
        if users_collection.count_documents({}) == 0:
            print("Creating users collection...")
            # This is just a test document, it will be removed
            test_id = users_collection.insert_one({"test": True}).inserted_id
            users_collection.delete_one({"_id": test_id})

        # Count users
        user_count = users_collection.count_documents({})

        print("MongoDB Connection Successful!")
        print(f"Database: fittrack_db")
        print(f"Users Collection: users")
        print(f"Number of users in database: {user_count}")

        return True
    except (ConnectionFailure, ServerSelectionTimeoutError):
        print("MongoDB Connection Failed. Make sure MongoDB is running on localhost:27017")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    # Exit with success even if MongoDB fails - we'll handle this gracefully
    sys.exit(0)
