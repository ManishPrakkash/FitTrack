"""
Direct MongoDB authentication module for FitTrack.
"""
import os
import json
import hashlib
import datetime
import jwt
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://manishprakkash:HYeLg73wjj0593Gy@fitrack-db.9hmlhdb.mongodb.net/?retryWrites=true&w=majority&appName=fitrack-db&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&socketTimeoutMS=10000&maxPoolSize=10&retryReads=true')
DB_NAME = 'fittrack_db'
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-key-for-development-only')

# Connect to MongoDB with better error handling
try:
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
        maxPoolSize=10,
        retryWrites=True,
        retryReads=True
    )
    # Test the connection
    client.admin.command('ping')
    db = client[DB_NAME]
    print("✓ MongoDB connection successful")
except Exception as e:
    print(f"✗ MongoDB connection failed: {e}")
    # Create a dummy client for development
    client = None
    db = None

# Collections
users_collection = db['users'] if db else None
profiles_collection = db['profiles'] if db else None
challenges_collection = db['challenges'] if db else None
activities_collection = db['activities'] if db else None
challenge_participants_collection = db['challenge_participants'] if db else None

class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles MongoDB ObjectId."""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against a provided password."""
    return stored_password == hash_password(provided_password)

def generate_token(user_id):
    """Generate a JWT token for the given user ID."""
    payload = {
        'id': str(user_id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token

def verify_token(token):
    """Verify a JWT token and return the user ID."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def register_user(name, email, password, username=None):
    """Register a new user."""
    # Check if user already exists
    if users_collection.find_one({'email': email}):
        return {
            'success': False,
            'message': 'Email already exists'
        }

    # Create username if not provided
    if not username:
        username = email.split('@')[0]

    # Create user document
    user = {
        'name': name,
        'email': email,
        'username': username,
        'password': hash_password(password),
        'date_joined': datetime.datetime.utcnow(),
        'is_active': True
    }

    # Insert user
    user_id = users_collection.insert_one(user).inserted_id

    # Create profile
    profile = {
        'user_id': user_id,
        'name': name,
        'height': None,
        'weight': None,
        'age': None,
        'gender': None,
        'fitness_goal': None,
        'activity_level': None
    }

    # Insert profile
    profiles_collection.insert_one(profile)

    return {
        'success': True,
        'message': 'User registered successfully'
    }

def login_user(email, password):
    """Login a user."""
    # Find user
    user = users_collection.find_one({'email': email})

    if not user:
        return {
            'success': False,
            'message': 'User not found'
        }

    # Verify password
    if not verify_password(user['password'], password):
        return {
            'success': False,
            'message': 'Invalid credentials'
        }

    # Generate token
    token = generate_token(user['_id'])

    # Get profile
    profile = profiles_collection.find_one({'user_id': user['_id']})

    # Prepare user data
    user_data = {
        'id': str(user['_id']),
        'name': user.get('name', ''),
        'email': user['email'],
        'username': user['username'],
        'date_joined': user['date_joined'].isoformat(),
        'profile': {
            'name': profile.get('name', '') if profile else '',
            'height': profile.get('height') if profile else None,
            'weight': profile.get('weight') if profile else None,
            'age': profile.get('age') if profile else None,
            'gender': profile.get('gender') if profile else None,
            'fitness_goal': profile.get('fitness_goal') if profile else None,
            'activity_level': profile.get('activity_level') if profile else None
        }
    }

    return {
        'success': True,
        'token': token,
        'user': user_data
    }

def get_user_by_token(token):
    """Get user by token."""
    user_id = verify_token(token)

    if not user_id:
        return None

    # Find user
    user = users_collection.find_one({'_id': ObjectId(user_id)})

    if not user:
        return None

    # Get profile
    profile = profiles_collection.find_one({'user_id': user['_id']})

    # Prepare user data
    user_data = {
        'id': str(user['_id']),
        'name': user.get('name', ''),
        'email': user['email'],
        'username': user['username'],
        'date_joined': user['date_joined'].isoformat(),
        'profile': {
            'name': profile.get('name', '') if profile else '',
            'height': profile.get('height') if profile else None,
            'weight': profile.get('weight') if profile else None,
            'age': profile.get('age') if profile else None,
            'gender': profile.get('gender') if profile else None,
            'fitness_goal': profile.get('fitness_goal') if profile else None,
            'activity_level': profile.get('activity_level') if profile else None
        }
    }

    return user_data

# Challenge Management Functions

def create_challenge(name, challenge_type, description, goal, unit, created_by_id):
    """Create a new challenge."""
    try:
        challenge = {
            'name': name,
            'type': challenge_type,
            'description': description,
            'goal': float(goal),
            'unit': unit,
            'created_by': ObjectId(created_by_id),
            'created_at': datetime.datetime.utcnow(),
            'updated_at': datetime.datetime.utcnow(),
            'is_active': True
        }

        challenge_id = challenges_collection.insert_one(challenge).inserted_id

        # Return the created challenge with ID
        challenge['_id'] = challenge_id
        return {
            'success': True,
            'challenge': challenge,
            'message': 'Challenge created successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error creating challenge: {str(e)}'
        }

def get_all_challenges():
    """Get all active challenges."""
    try:
        challenges = list(challenges_collection.find({'is_active': True}).sort('created_at', -1))

        # Convert ObjectIds to strings and add participant count
        for challenge in challenges:
            challenge['id'] = str(challenge['_id'])
            challenge['created_by'] = str(challenge['created_by'])

            # Count participants
            participant_count = challenge_participants_collection.count_documents({
                'challenge_id': challenge['_id']
            })
            challenge['participants'] = participant_count

            # Convert dates to ISO format
            challenge['created_at'] = challenge['created_at'].isoformat()
            challenge['updated_at'] = challenge['updated_at'].isoformat()

        return {
            'success': True,
            'challenges': challenges
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error fetching challenges: {str(e)}'
        }

def get_challenge_by_id(challenge_id):
    """Get a specific challenge by ID."""
    try:
        challenge = challenges_collection.find_one({'_id': ObjectId(challenge_id), 'is_active': True})

        if not challenge:
            return {
                'success': False,
                'message': 'Challenge not found'
            }

        challenge['id'] = str(challenge['_id'])
        challenge['created_by'] = str(challenge['created_by'])

        # Count participants
        participant_count = challenge_participants_collection.count_documents({
            'challenge_id': challenge['_id']
        })
        challenge['participants'] = participant_count

        # Convert dates to ISO format
        challenge['created_at'] = challenge['created_at'].isoformat()
        challenge['updated_at'] = challenge['updated_at'].isoformat()

        return {
            'success': True,
            'challenge': challenge
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error fetching challenge: {str(e)}'
        }

def update_challenge(challenge_id, name=None, challenge_type=None, description=None, goal=None, unit=None):
    """Update an existing challenge."""
    try:
        update_data = {'updated_at': datetime.datetime.utcnow()}

        if name is not None:
            update_data['name'] = name
        if challenge_type is not None:
            update_data['type'] = challenge_type
        if description is not None:
            update_data['description'] = description
        if goal is not None:
            update_data['goal'] = float(goal)
        if unit is not None:
            update_data['unit'] = unit

        result = challenges_collection.update_one(
            {'_id': ObjectId(challenge_id), 'is_active': True},
            {'$set': update_data}
        )

        if result.matched_count == 0:
            return {
                'success': False,
                'message': 'Challenge not found'
            }

        return {
            'success': True,
            'message': 'Challenge updated successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error updating challenge: {str(e)}'
        }

def delete_challenge(challenge_id):
    """Soft delete a challenge (mark as inactive)."""
    try:
        result = challenges_collection.update_one(
            {'_id': ObjectId(challenge_id)},
            {'$set': {'is_active': False, 'updated_at': datetime.datetime.utcnow()}}
        )

        if result.matched_count == 0:
            return {
                'success': False,
                'message': 'Challenge not found'
            }

        return {
            'success': True,
            'message': 'Challenge deleted successfully'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error deleting challenge: {str(e)}'
        }

# Challenge Participation Functions

def join_challenge(user_id, challenge_id):
    """Join a user to a challenge."""
    try:
        # Check if user already joined
        existing = challenge_participants_collection.find_one({
            'user_id': ObjectId(user_id),
            'challenge_id': ObjectId(challenge_id)
        })

        if existing:
            return {
                'success': False,
                'message': 'You have already joined this challenge'
            }

        # Check if challenge exists
        challenge = challenges_collection.find_one({'_id': ObjectId(challenge_id), 'is_active': True})
        if not challenge:
            return {
                'success': False,
                'message': 'Challenge not found'
            }

        # Create participation record
        participant = {
            'user_id': ObjectId(user_id),
            'challenge_id': ObjectId(challenge_id),
            'current_progress': 0.0,
            'joined_at': datetime.datetime.utcnow(),
            'completed': False,
            'completed_at': None
        }

        challenge_participants_collection.insert_one(participant)

        return {
            'success': True,
            'message': 'Successfully joined the challenge'
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error joining challenge: {str(e)}'
        }

def get_user_challenges(user_id, challenge_type='all'):
    """Get challenges for a user (joined, available, or all)."""
    try:
        if challenge_type == 'joined':
            # Get challenges the user has joined
            participants = list(challenge_participants_collection.find({'user_id': ObjectId(user_id)}))
            challenge_ids = [p['challenge_id'] for p in participants]

            if not challenge_ids:
                return {
                    'success': True,
                    'challenges': []
                }

            challenges = list(challenges_collection.find({
                '_id': {'$in': challenge_ids},
                'is_active': True
            }).sort('created_at', -1))

            # Add progress information
            for challenge in challenges:
                participant = next((p for p in participants if p['challenge_id'] == challenge['_id']), None)
                if participant:
                    challenge['current_progress'] = participant['current_progress']
                    challenge['progress_percentage'] = min(
                        round((participant['current_progress'] / challenge['goal']) * 100), 100
                    ) if challenge['goal'] > 0 else 0
                    challenge['is_joined'] = True
                    challenge['completed'] = participant['completed']

        elif challenge_type == 'available':
            # Get challenges the user hasn't joined
            joined_challenge_ids = [
                p['challenge_id'] for p in
                challenge_participants_collection.find({'user_id': ObjectId(user_id)})
            ]

            challenges = list(challenges_collection.find({
                '_id': {'$nin': joined_challenge_ids},
                'is_active': True
            }).sort('created_at', -1))

            for challenge in challenges:
                challenge['is_joined'] = False
                challenge['current_progress'] = 0
                challenge['progress_percentage'] = 0

        else:  # all challenges
            challenges = list(challenges_collection.find({'is_active': True}).sort('created_at', -1))

            # Get user's participation data
            participants = {
                p['challenge_id']: p for p in
                challenge_participants_collection.find({'user_id': ObjectId(user_id)})
            }

            for challenge in challenges:
                participant = participants.get(challenge['_id'])
                if participant:
                    challenge['current_progress'] = participant['current_progress']
                    challenge['progress_percentage'] = min(
                        round((participant['current_progress'] / challenge['goal']) * 100), 100
                    ) if challenge['goal'] > 0 else 0
                    challenge['is_joined'] = True
                    challenge['completed'] = participant['completed']
                else:
                    challenge['is_joined'] = False
                    challenge['current_progress'] = 0
                    challenge['progress_percentage'] = 0
                    challenge['completed'] = False

        # Format challenges for response
        for challenge in challenges:
            challenge['id'] = str(challenge['_id'])
            challenge['created_by'] = str(challenge['created_by'])

            # Count total participants
            participant_count = challenge_participants_collection.count_documents({
                'challenge_id': challenge['_id']
            })
            challenge['participants'] = participant_count

            # Convert dates to ISO format
            challenge['created_at'] = challenge['created_at'].isoformat()
            challenge['updated_at'] = challenge['updated_at'].isoformat()

        return {
            'success': True,
            'challenges': challenges
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error fetching user challenges: {str(e)}'
        }

# Activity Management Functions

def log_activity(user_id, challenge_id, value, notes=None):
    """Log an activity for a user in a challenge."""
    try:
        # Check if user is participating in the challenge
        participant = challenge_participants_collection.find_one({
            'user_id': ObjectId(user_id),
            'challenge_id': ObjectId(challenge_id)
        })

        if not participant:
            return {
                'success': False,
                'message': 'You must join the challenge before logging activities'
            }

        # Get challenge details
        challenge = challenges_collection.find_one({'_id': ObjectId(challenge_id), 'is_active': True})
        if not challenge:
            return {
                'success': False,
                'message': 'Challenge not found'
            }

        # Create activity record
        activity = {
            'user_id': ObjectId(user_id),
            'challenge_id': ObjectId(challenge_id),
            'value': float(value),
            'notes': notes,
            'date': datetime.datetime.utcnow().date(),
            'created_at': datetime.datetime.utcnow()
        }

        activities_collection.insert_one(activity)

        # Update participant progress
        new_progress = participant['current_progress'] + float(value)
        completed = new_progress >= challenge['goal']

        update_data = {
            'current_progress': new_progress,
            'completed': completed
        }

        if completed and not participant['completed']:
            update_data['completed_at'] = datetime.datetime.utcnow()

        challenge_participants_collection.update_one(
            {'_id': participant['_id']},
            {'$set': update_data}
        )

        return {
            'success': True,
            'message': 'Activity logged successfully',
            'new_progress': new_progress,
            'completed': completed
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error logging activity: {str(e)}'
        }

def get_user_activities(user_id, challenge_id=None):
    """Get activities for a user, optionally filtered by challenge."""
    try:
        query = {'user_id': ObjectId(user_id)}
        if challenge_id:
            query['challenge_id'] = ObjectId(challenge_id)

        activities = list(activities_collection.find(query).sort('created_at', -1))

        # Format activities for response
        for activity in activities:
            activity['id'] = str(activity['_id'])
            activity['user_id'] = str(activity['user_id'])
            activity['challenge_id'] = str(activity['challenge_id'])

            # Get challenge name
            challenge = challenges_collection.find_one({'_id': activity['challenge_id']})
            if challenge:
                activity['challenge_name'] = challenge['name']
                activity['challenge_unit'] = challenge['unit']

            # Convert dates to ISO format
            activity['date'] = activity['date'].isoformat() if hasattr(activity['date'], 'isoformat') else str(activity['date'])
            activity['created_at'] = activity['created_at'].isoformat()

        return {
            'success': True,
            'activities': activities
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error fetching activities: {str(e)}'
        }

def get_challenge_leaderboard(challenge_id):
    """Get leaderboard for a challenge."""
    try:
        # Get all participants for the challenge
        participants = list(challenge_participants_collection.find({
            'challenge_id': ObjectId(challenge_id)
        }).sort('current_progress', -1))

        leaderboard = []
        for i, participant in enumerate(participants):
            # Get user details
            user = users_collection.find_one({'_id': participant['user_id']})
            if user:
                leaderboard.append({
                    'rank': i + 1,
                    'user_name': user.get('name', 'Unknown'),
                    'progress': participant['current_progress'],
                    'completed': participant['completed'],
                    'joined_at': participant['joined_at'].isoformat()
                })

        return {
            'success': True,
            'leaderboard': leaderboard
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error fetching leaderboard: {str(e)}'
        }
