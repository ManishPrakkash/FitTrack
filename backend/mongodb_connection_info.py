#!/usr/bin/env python3
"""
MongoDB Connection Information
"""

from pymongo import MongoClient
import socket
import sys
import json
from bson import json_util

def get_mongodb_connection_info():
    """Get MongoDB connection information"""
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        
        # Test connection
        server_info = client.admin.command('ismaster')
        
        # Get host information
        hostname = socket.gethostname()
        host_ip = socket.gethostbyname(hostname)
        
        # Get MongoDB version
        build_info = client.admin.command('buildInfo')
        mongodb_version = build_info.get('version', 'Unknown')
        
        # Get database information
        databases = client.list_database_names()
        db_info = {}
        
        for db_name in databases:
            db = client[db_name]
            collections = db.list_collection_names()
            collection_info = {}
            
            for coll_name in collections:
                collection = db[coll_name]
                doc_count = collection.count_documents({})
                collection_info[coll_name] = {
                    'document_count': doc_count
                }
            
            db_info[db_name] = {
                'collections': collection_info
            }
        
        # Print connection information
        print("\n=== MONGODB CONNECTION INFORMATION ===\n")
        print(f"MongoDB Version: {mongodb_version}")
        print(f"Hostname: {hostname}")
        print(f"Host IP: {host_ip}")
        print(f"Connection String: mongodb://localhost:27017/")
        print(f"Connected to: {server_info.get('me', 'Unknown')}")
        
        # Print database information
        print("\n=== DATABASES ===\n")
        for db_name, db_data in db_info.items():
            print(f"Database: {db_name}")
            collections = db_data['collections']
            if collections:
                print("  Collections:")
                for coll_name, coll_data in collections.items():
                    print(f"    - {coll_name} ({coll_data['document_count']} documents)")
            else:
                print("  No collections")
            print()
        
        # Check specifically for fittrack_db
        if 'fittrack_db' in databases:
            print("\n=== FITTRACK DATABASE ===\n")
            print("The fittrack_db database exists!")
            
            # Check for users collection
            if 'users' in db_info.get('fittrack_db', {}).get('collections', {}):
                print("The users collection exists!")
                user_count = db_info['fittrack_db']['collections']['users']['document_count']
                print(f"There are {user_count} users in the database.")
                
                # Show a sample user
                if user_count > 0:
                    print("\nSample user:")
                    user = client['fittrack_db']['users'].find_one()
                    user_json = json_util.loads(json_util.dumps(user))
                    for key, value in user_json.items():
                        if key != '_id':  # Skip the MongoDB ObjectId
                            print(f"  {key}: {value}")
            else:
                print("The users collection does not exist!")
        else:
            print("\n=== FITTRACK DATABASE ===\n")
            print("The fittrack_db database does not exist!")
        
        # Connection instructions
        print("\n=== CONNECTION INSTRUCTIONS ===\n")
        print("To connect to this MongoDB instance using MongoDB Compass:")
        print("1. Open MongoDB Compass")
        print("2. Enter the connection string: mongodb://localhost:27017/")
        print("3. Click 'Connect'")
        print("4. Look for 'fittrack_db' in the list of databases")
        print("5. Click on 'fittrack_db' to see its collections")
        print("6. Click on 'users' to see the user data")
        
        return True
    
    except Exception as e:
        print(f"\nError connecting to MongoDB: {str(e)}")
        return False

if __name__ == "__main__":
    success = get_mongodb_connection_info()
    sys.exit(0 if success else 1)
