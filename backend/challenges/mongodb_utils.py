from pymongo import MongoClient
from bson.objectid import ObjectId
import uuid
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['fitrack_db']
challenges_collection = db['challenges']
user_progress_collection = db['user_progress']
users_collection = db['users']

def create_challenge(name, type, description, goal, unit, created_by):
    """
    Create a new challenge in MongoDB
    """
    challenge = {
        'id': str(uuid.uuid4()),
        'name': name,
        'type': type,
        'description': description,
        'goal': float(goal),
        'unit': unit,
        'created_by': created_by,
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }

    result = challenges_collection.insert_one(challenge)

    if result.inserted_id:
        return challenge
    return None

def get_all_challenges():
    """
    Get all challenges
    """
    challenges = list(challenges_collection.find({}, {'_id': 0}))
    return challenges

def get_challenge_by_id(challenge_id):
    """
    Get challenge by ID
    """
    challenge = challenges_collection.find_one({'id': challenge_id}, {'_id': 0})
    return challenge

def delete_challenge(challenge_id):
    """
    Delete challenge by ID
    """
    result = challenges_collection.delete_one({'id': challenge_id})
    return result.deleted_count > 0

def create_or_update_progress(user_id, challenge_id, current_value):
    """
    Create or update user progress for a challenge
    """
    # Check if progress already exists
    existing_progress = user_progress_collection.find_one({
        'user_id': user_id,
        'challenge_id': challenge_id
    })

    if existing_progress:
        # Update existing progress
        result = user_progress_collection.update_one(
            {'user_id': user_id, 'challenge_id': challenge_id},
            {'$set': {'current_value': float(current_value), 'last_updated': datetime.now()}}
        )
        if result.modified_count > 0:
            return get_user_challenge_progress(user_id, challenge_id)
    else:
        # Create new progress
        progress = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'challenge_id': challenge_id,
            'current_value': float(current_value),
            'joined_at': datetime.now(),
            'last_updated': datetime.now()
        }

        result = user_progress_collection.insert_one(progress)

        if result.inserted_id:
            progress.pop('_id', None)
            return progress

    return None

def get_user_progress(user_id):
    """
    Get all progress for a specific user
    """
    progress = list(user_progress_collection.find({'user_id': user_id}, {'_id': 0}))
    return progress

def get_user_challenge_progress(user_id, challenge_id):
    """
    Get progress for a specific user and challenge
    """
    progress = user_progress_collection.find_one(
        {'user_id': user_id, 'challenge_id': challenge_id},
        {'_id': 0}
    )
    return progress

def get_challenge_leaderboard(challenge_id):
    """
    Get leaderboard for a specific challenge
    """
    # Get the challenge to get the unit
    challenge = get_challenge_by_id(challenge_id)
    if not challenge:
        return []

    # Get all progress entries for this challenge
    progress_entries = list(user_progress_collection.find({'challenge_id': challenge_id}, {'_id': 0}))

    # Create leaderboard entries with user information
    leaderboard = []
    for entry in progress_entries:
        user = users_collection.find_one({'id': entry['user_id']}, {'_id': 0})
        if user:
            name_parts = user['name'].split()
            avatar_text = ''.join([part[0].upper() for part in name_parts if part])

            leaderboard.append({
                'user_id': user['id'],
                'name': user['name'],
                'avatar_text': avatar_text,
                'score': entry['current_value'],
                'unit': challenge['unit']
            })

    # Sort by score (descending)
    leaderboard.sort(key=lambda x: x['score'], reverse=True)

    return leaderboard
