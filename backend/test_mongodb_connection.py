"""
Test script to check MongoDB Atlas connection.
"""
import os
import sys
import django
from pymongo import MongoClient
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack_backend.settings')
django.setup()

def test_mongodb_connection():
    """Test the connection to MongoDB Atlas."""
    print("Testing MongoDB Atlas connection...")
    
    # Get MongoDB connection details from Django settings
    mongodb_uri = settings.DATABASES['default']['CLIENT']['host']
    username = settings.DATABASES['default']['CLIENT']['username']
    password = settings.DATABASES['default']['CLIENT']['password']
    
    print(f"MongoDB URI: {mongodb_uri}")
    
    try:
        # Connect to MongoDB Atlas
        client = MongoClient(mongodb_uri)
        
        # List all databases to test connection
        databases = client.list_database_names()
        print(f"Connected to MongoDB Atlas successfully!")
        print(f"Available databases: {databases}")
        
        # Get the database
        db = client[settings.DATABASES['default']['NAME']]
        print(f"Using database: {db.name}")
        
        # List all collections
        collections = db.list_collection_names()
        print(f"Collections in database: {collections}")
        
        # Test creating a test collection
        if 'test_connection' not in collections:
            db.create_collection('test_connection')
            print("Created test_connection collection")
        
        # Insert a test document
        test_collection = db['test_connection']
        result = test_collection.insert_one({
            'test': 'Connection successful',
            'timestamp': django.utils.timezone.now().isoformat()
        })
        print(f"Inserted test document with ID: {result.inserted_id}")
        
        # Retrieve the test document
        test_doc = test_collection.find_one({'_id': result.inserted_id})
        print(f"Retrieved test document: {test_doc}")
        
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        return False

if __name__ == "__main__":
    success = test_mongodb_connection()
    sys.exit(0 if success else 1)
