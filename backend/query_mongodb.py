#!/usr/bin/env python3
"""
MongoDB Query Tool for FitTrack

This script allows you to interact with the FitTrack MongoDB database
and perform various queries on the data.
"""

import sys
import json
from pymongo import MongoClient
from bson import json_util, ObjectId

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fittrack_db']

def parse_json(data):
    """Convert MongoDB objects to JSON"""
    return json.loads(json_util.dumps(data))

def print_document(doc):
    """Print a document in a readable format"""
    doc_json = parse_json(doc)
    for key, value in doc_json.items():
        if key != '_id':  # Skip the MongoDB ObjectId
            print(f"{key}: {value}")
    print("-" * 50)

def list_databases():
    """List all databases in MongoDB"""
    print("\n=== DATABASES ===\n")
    for db_name in client.list_database_names():
        print(f"- {db_name}")

def list_collections():
    """List all collections in the fittrack_db database"""
    print("\n=== COLLECTIONS IN fittrack_db ===\n")
    for collection in db.list_collection_names():
        print(f"- {collection}")
        # Count documents in each collection
        count = db[collection].count_documents({})
        print(f"  ({count} documents)")

def view_all_users():
    """View all users in the database"""
    users = list(db.users.find())
    print(f"\n=== ALL USERS ({len(users)}) ===\n")
    
    for user in users:
        print_document(user)

def find_user_by_email(email):
    """Find a user by email"""
    user = db.users.find_one({"email": email})
    
    if user:
        print(f"\n=== USER WITH EMAIL: {email} ===\n")
        print_document(user)
    else:
        print(f"\nNo user found with email: {email}")

def find_user_by_name(name):
    """Find users by name (partial match)"""
    # Using a case-insensitive regex to find partial matches
    users = list(db.users.find({"name": {"$regex": name, "$options": "i"}}))
    
    if users:
        print(f"\n=== USERS WITH NAME CONTAINING: {name} ({len(users)}) ===\n")
        for user in users:
            print_document(user)
    else:
        print(f"\nNo users found with name containing: {name}")

def show_help():
    """Show help information"""
    print("\n=== MONGODB QUERY TOOL FOR FITTRACK ===\n")
    print("Usage: python query_mongodb.py [COMMAND] [ARGS]\n")
    print("Commands:")
    print("  dbs                     List all databases")
    print("  collections             List all collections in fittrack_db")
    print("  users                   View all users")
    print("  email [EMAIL]           Find user by email")
    print("  name [NAME]             Find users by name (partial match)")
    print("  help                    Show this help message")
    print("\nExamples:")
    print("  python query_mongodb.py users")
    print("  python query_mongodb.py email test@example.com")
    print("  python query_mongodb.py name john")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        show_help()
    elif sys.argv[1] == "dbs":
        list_databases()
    elif sys.argv[1] == "collections":
        list_collections()
    elif sys.argv[1] == "users":
        view_all_users()
    elif sys.argv[1] == "email" and len(sys.argv) > 2:
        find_user_by_email(sys.argv[2])
    elif sys.argv[1] == "name" and len(sys.argv) > 2:
        find_user_by_name(sys.argv[2])
    else:
        print("Invalid command. Use 'python query_mongodb.py help' for usage information.")
