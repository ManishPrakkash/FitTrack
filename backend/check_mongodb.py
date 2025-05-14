import subprocess
import sys
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def check_mongodb_running():
    """Check if MongoDB is running."""
    try:
        # Try to connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=1000)
        client.admin.command('ismaster')
        print("MongoDB is running.")
        return True
    except ConnectionFailure:
        print("MongoDB is not running.")
        return False

def start_mongodb():
    """Try to start MongoDB."""
    try:
        print("Attempting to start MongoDB...")
        # This will only work if MongoDB is installed
        subprocess.Popen(['mongod', '--dbpath', '/tmp/data/db'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
        
        # Wait for MongoDB to start
        for _ in range(5):
            time.sleep(1)
            if check_mongodb_running():
                return True
        
        print("Failed to start MongoDB after waiting.")
        return False
    except Exception as e:
        print(f"Error starting MongoDB: {e}")
        return False

if __name__ == "__main__":
    if not check_mongodb_running():
        if not start_mongodb():
            print("Could not start MongoDB. Please make sure it's installed and try again.")
            print("For this application to work, MongoDB must be running on localhost:27017")
            sys.exit(1)
    
    print("MongoDB connection successful. You can now run the Django server.")
