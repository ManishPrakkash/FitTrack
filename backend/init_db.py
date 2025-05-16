"""
Database initialization script for FitTrack.
This script sets up the MongoDB collections and indexes directly,
bypassing Django's migration system which has compatibility issues with djongo.
"""
import os
import sys
import pymongo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_database():
    """Initialize the MongoDB database with required collections and indexes."""
    print("Initializing MongoDB database...")
    
    # Check if we should use MongoDB Atlas
    use_atlas = os.getenv('USE_MONGODB_ATLAS', 'False') == 'True'
    
    if use_atlas:
        print("Using MongoDB Atlas...")
        connection_string = os.getenv('MONGODB_URI', 'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db')
    else:
        print("Using local MongoDB...")
        connection_string = 'mongodb://localhost:27017'
    
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        
        # Verify connection
        client.admin.command('ping')
        print('MongoDB connection successful!')
        
        # Get or create database
        db_name = os.getenv('MONGODB_NAME', 'fittrack_db')
        db = client[db_name]
        print(f"Using database: {db_name}")
        
        # Create collections if they don't exist
        if 'users' not in db.list_collection_names():
            print("Creating users collection...")
            users = db.create_collection('users')
            # Create indexes
            users.create_index([('email', pymongo.ASCENDING)], unique=True)
            print("Created users collection with email index")
        else:
            print("Users collection already exists")
        
        # Create django_migrations collection to track migrations
        if 'django_migrations' not in db.list_collection_names():
            print("Creating django_migrations collection...")
            db.create_collection('django_migrations')
            print("Created django_migrations collection")
        else:
            print("django_migrations collection already exists")
        
        # Create django_content_type collection
        if 'django_content_type' not in db.list_collection_names():
            print("Creating django_content_type collection...")
            db.create_collection('django_content_type')
            print("Created django_content_type collection")
        else:
            print("django_content_type collection already exists")
        
        # Create auth_permission collection
        if 'auth_permission' not in db.list_collection_names():
            print("Creating auth_permission collection...")
            db.create_collection('auth_permission')
            print("Created auth_permission collection")
        else:
            print("auth_permission collection already exists")
        
        print("Database initialization completed successfully!")
        return True
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if not success:
        sys.exit(1)
