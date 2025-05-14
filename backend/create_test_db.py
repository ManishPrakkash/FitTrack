from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Create a test database and collection
db = client['test_database']
collection = db['test_collection']

# Insert a test document
result = collection.insert_one({"name": "Test Document", "value": 123})

print(f"Inserted document with ID: {result.inserted_id}")

# List all databases to confirm creation
print("\nAll databases:")
for db_name in client.list_database_names():
    print(f"- {db_name}")

print("\nTest complete. The test_database should now be visible in MongoDB.")
