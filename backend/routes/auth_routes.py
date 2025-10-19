from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
from utils.auth import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Pydantic models
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    subscription_plan: str
    created_at: str

# Dependency to get current user from token
async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Not authenticated')
    
    token = authorization.split(' ')[1]
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid or expired token')
    
    user = await db.users.find_one({'email': payload.get('sub')})
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    
    return user

@router.post('/register')
async def register(user_data: UserRegister):
    \"\"\"Register a new user\"\"\"
    # Check if user already exists
    existing_user = await db.users.find_one({'email': user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    
    new_user = {
        'email': user_data.email,
        'name': user_data.name,
        'password': hashed_password,
        'subscription_plan': 'free',
        'videos_created': 0,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    result = await db.users.insert_one(new_user)
    
    # Create access token
    access_token = create_access_token(data={'sub': user_data.email})
    
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            'id': str(result.inserted_id),
            'email': user_data.email,
            'name': user_data.name,
            'subscription_plan': 'free'
        }
    }

@router.post('/login')
async def login(user_data: UserLogin):
    \"\"\"Login user\"\"\"
    # Find user
    user = await db.users.find_one({'email': user_data.email})
    if not user:
        raise HTTPException(status_code=401, detail='Invalid email or password')
    
    # Verify password
    if not verify_password(user_data.password, user['password']):
        raise HTTPException(status_code=401, detail='Invalid email or password')
    
    # Create access token
    access_token = create_access_token(data={'sub': user_data.email})
    
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {
            'id': str(user['_id']),
            'email': user['email'],
            'name': user['name'],
            'subscription_plan': user.get('subscription_plan', 'free')
        }
    }

@router.get('/me')
async def get_current_user_info(current_user = Depends(get_current_user)):
    \"\"\"Get current user information\"\"\"
    return {
        'id': str(current_user['_id']),
        'email': current_user['email'],
        'name': current_user['name'],
        'subscription_plan': current_user.get('subscription_plan', 'free'),
        'videos_created': current_user.get('videos_created', 0),
        'created_at': current_user.get('created_at')
    }
