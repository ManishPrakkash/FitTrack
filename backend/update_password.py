import os
import django
from pymongo import MongoClient

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fittrack_backend.settings")
django.setup()

# Now we can import Django modules
from django.contrib.auth.hashers import make_password

# Email to update
email_to_update = "Manish@gmail.com"
new_password = "password123"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['fitrack_db']
users_collection = db['users']

# Find the user
user = users_collection.find_one({"email": email_to_update})

if user:
    print(f"User found with email: {email_to_update}")

    # Hash the new password
    hashed_password = make_password(new_password)

    # Update the password
    result = users_collection.update_one(
        {"email": email_to_update},
        {"$set": {"password": hashed_password}}
    )

    if result.modified_count > 0:
        print(f"Password updated successfully for {email_to_update}")
        print(f"New password is: {new_password}")
    else:
        print("Password update failed")
else:
    print(f"No user found with email: {email_to_update}")
