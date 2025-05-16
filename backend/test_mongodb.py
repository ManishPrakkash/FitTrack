"""
Test script to verify MongoDB connection.
"""
import pymongo
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_mongodb_connection():
    """Test connection to MongoDB."""
    print("Testing MongoDB connection...")

    # Check if we should use MongoDB Atlas
    use_atlas = os.getenv('USE_MONGODB_ATLAS', 'False') == 'True'

    if use_atlas:
        print("Testing MongoDB Atlas connection...")
        connection_string = os.getenv('MONGODB_URI', 'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db')
    else:
        print("Testing local MongoDB connection...")
        connection_string = 'mongodb://localhost:27017'

    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=5000)

        # Verify connection
        client.admin.command('ping')
        print('MongoDB connection successful!')

        # Get database information
        db_names = client.list_database_names()
        print(f"Available databases: {db_names}")

        # Create or access the fittrack_db database
        db_name = os.getenv('MONGODB_NAME', 'fittrack_db')
        db = client[db_name]
        print(f"Using database: {db_name}")

        # List collections in the database
        collections = db.list_collection_names()
        print(f"Collections in {db_name}: {collections}")

        return True
    except Exception as e:
        print(f'MongoDB connection failed: {e}')
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    if not success:
        print("\nTroubleshooting tips:")
        print("1. Make sure Docker is running")
        print("2. Check if the MongoDB container is running: docker ps")
        print("3. If needed, start the MongoDB container: docker-compose up -d")
        print("4. If using MongoDB Atlas, check your network connection and firewall settings")
        sys.exit(1)
