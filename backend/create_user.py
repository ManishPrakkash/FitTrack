"""
Direct MongoDB user creation script for FitTrack.
This script creates a user directly in MongoDB, bypassing Django's ORM.
"""
import os
import sys
import getpass
import pymongo
import bcrypt
from datetime import datetime
from dotenv import load_dotenv
from bson.objectid import ObjectId

# Load environment variables
load_dotenv()

def create_user():
    """Create a user directly in MongoDB."""
    print("Creating user directly in MongoDB...")
    
    # Get user input
    email = input("Email: ")
    name = input("Name: ")
    password = getpass.getpass("Password: ")
    is_admin = input("Create as admin? (y/n): ").lower() == 'y'
    
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
        
        # Get database
        db_name = os.getenv('MONGODB_NAME', 'fittrack_db')
        db = client[db_name]
        print(f"Using database: {db_name}")
        
        # Check if users collection exists
        if 'users' not in db.list_collection_names():
            print("Creating users collection...")
            users = db.create_collection('users')
            # Create indexes
            users.create_index([('email', pymongo.ASCENDING)], unique=True)
            print("Created users collection with email index")
        
        # Check if user already exists
        existing_user = db.users.find_one({'email': email})
        if existing_user:
            print(f"Error: User with email {email} already exists")
            return False
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user document
        user_id = ObjectId()
        user_doc = {
            '_id': user_id,
            'email': email,
            'name': name,
            'password': hashed_password,
            'is_active': True,
            'is_staff': is_admin,
            'is_superuser': is_admin,
            'date_joined': datetime.utcnow()
        }
        
        # Insert user
        result = db.users.insert_one(user_doc)
        
        if result.inserted_id:
            print(f"User {email} created successfully with ID: {user_id}")
            return True
        else:
            print("Error: Failed to insert user")
            return False
            
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

if __name__ == "__main__":
    success = create_user()
    if not success:
        sys.exit(1)
