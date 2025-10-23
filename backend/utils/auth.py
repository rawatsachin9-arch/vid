from datetime import datetime, timedelta
from typing import Optional
import jwt
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-this')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode JWT access token"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# FastAPI dependency for getting current user from token or session
from fastapi import HTTPException, Request
from pymongo import MongoClient
from datetime import timezone

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "test_database")
_client = MongoClient(MONGO_URL)
_db = _client[DB_NAME]

async def get_current_user_from_token(request: Request):
    """
    Get current user from JWT token or session token
    Checks both Authorization header and session cookie
    """
    # Try to get JWT token from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        
        # Check if it's a session token
        session = _db.user_sessions.find_one({'session_token': token})
        if session:
            # Check if session expired
            expires_at = session['expires_at']
            if expires_at.tzinfo is None:
                # If stored as naive datetime, assume UTC
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            
            if expires_at < datetime.now(timezone.utc):
                _db.user_sessions.delete_one({'session_token': token})
                raise HTTPException(status_code=401, detail='Session expired')
            
            # Get user
            user = _db.users.find_one({'id': session['user_id']})
            if not user:
                user = _db.users.find_one({'_id': session['user_id']})
            
            if user:
                return {
                    'id': user.get('id') or str(user['_id']),
                    'email': user['email'],
                    'name': user['name']
                }
        
        # Otherwise, try JWT token
        payload = decode_access_token(token)
        if payload:
            user_email = payload.get('sub')
            user = _db.users.find_one({'email': user_email})
            if user:
                return {
                    'id': user.get('id') or str(user['_id']),
                    'email': user['email'],
                    'name': user['name']
                }
    
    # Try to get session token from cookie
    session_token = request.cookies.get('session_token')
    if session_token:
        session = _db.user_sessions.find_one({'session_token': session_token})
        if session:
            # Check if session expired
            expires_at = session['expires_at']
            if expires_at.tzinfo is None:
                # If stored as naive datetime, assume UTC
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            
            if expires_at < datetime.now(timezone.utc):
                _db.user_sessions.delete_one({'session_token': session_token})
                raise HTTPException(status_code=401, detail='Session expired')
            
            # Get user
            user = _db.users.find_one({'id': session['user_id']})
            if not user:
                user = _db.users.find_one({'_id': session['user_id']})
            
            if user:
                return {
                    'id': user.get('id') or str(user['_id']),
                    'email': user['email'],
                    'name': user['name']
                }
    
    raise HTTPException(status_code=401, detail='Not authenticated')
