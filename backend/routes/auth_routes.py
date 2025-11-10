from fastapi import APIRouter, HTTPException, Depends, Header, Response, Request
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone, timedelta
from utils.auth import hash_password, verify_password, create_access_token, decode_access_token
import httpx

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
    """Register a new user"""
    try:
        print(f"🔍 Registration attempt - Received user_data: {user_data}")
        print(f"📧 Email: {user_data.email}")
        print(f"👤 Name: {user_data.name}")
        print(f"🔒 Password length: {len(user_data.password)}")
        
        # Check if user already exists
        print(f"🔍 Checking if user exists with email: {user_data.email}")
        existing_user = await db.users.find_one({'email': user_data.email})
        
        if existing_user:
            print(f"❌ User already exists: {existing_user}")
            raise HTTPException(status_code=400, detail='Email already registered')
        
        print("✅ User doesn't exist, proceeding with registration")
        
        # Create new user
        print("🔒 Hashing password...")
        hashed_password = hash_password(user_data.password)
        print("✅ Password hashed successfully")
        
        new_user = {
            'email': user_data.email,
            'name': user_data.name,
            'password': hashed_password,
            'subscription_plan': 'free',
            'videos_created': 0,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        print(f"💾 Inserting new user into database: {new_user}")
        result = await db.users.insert_one(new_user)
        print(f"✅ User inserted with ID: {result.inserted_id}")
        
        # Create access token
        print("🎫 Creating access token...")
        access_token = create_access_token(data={'sub': user_data.email})
        print("✅ Access token created successfully")
        
        response_data = {
            'access_token': access_token,
            'token_type': 'bearer',
            'user': {
                'id': str(result.inserted_id),
                'email': user_data.email,
                'name': user_data.name,
                'subscription_plan': 'free'
            }
        }
        
        print(f"🎉 Registration successful, returning: {response_data}")
        return response_data
        
    except HTTPException as e:
        print(f"❌ HTTP Exception during registration: {e.detail}")
        raise e
    except Exception as e:
        print(f"💥 Unexpected error during registration: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f'Registration failed: {str(e)}')

@router.post('/login')
async def login(user_data: UserLogin):
    """Login user"""
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
    """Get current user information"""
    return {
        'id': str(current_user['_id']),
        'email': current_user['email'],
        'name': current_user['name'],
        'subscription_plan': current_user.get('subscription_plan', 'free'),
        'videos_created': current_user.get('videos_created', 0),
        'created_at': current_user.get('created_at')
    }

# Google OAuth Integration
@router.post('/google/session')
async def process_google_session(request: Request, response: Response):
    """Process Google OAuth session from Emergent Auth"""
    try:
        # Get session_id from request header
        session_id = request.headers.get('X-Session-ID')
        
        if not session_id:
            raise HTTPException(status_code=400, detail='Session ID required')
        
        # Call Emergent Auth API to get user data
        async with httpx.AsyncClient() as client:
            auth_response = await client.get(
                'https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data',
                headers={'X-Session-ID': session_id},
                timeout=10.0
            )
            
            if auth_response.status_code != 200:
                raise HTTPException(status_code=401, detail='Invalid session')
            
            user_data = auth_response.json()
        
        # Check if user exists in database
        existing_user = await db.users.find_one({'email': user_data['email']})
        
        if not existing_user:
            # Create new user
            new_user = {
                'id': user_data['id'],
                'email': user_data['email'],
                'name': user_data['name'],
                'picture': user_data.get('picture'),
                'subscription_plan': 'free',
                'videos_created': 0,
                'created_at': datetime.now(timezone.utc).isoformat(),
                'updated_at': datetime.now(timezone.utc).isoformat()
            }
            await db.users.insert_one(new_user)
            user_id = user_data['id']
        else:
            user_id = existing_user.get('id') or str(existing_user['_id'])
        
        # Store session in database
        session_token = user_data['session_token']
        session_doc = {
            'user_id': user_id,
            'session_token': session_token,
            'expires_at': datetime.now(timezone.utc) + timedelta(days=7),
            'created_at': datetime.now(timezone.utc)
        }
        await db.user_sessions.insert_one(session_doc)
        
        # Set httpOnly cookie
        response.set_cookie(
            key='session_token',
            value=session_token,
            httponly=True,
            secure=True,
            samesite='none',
            max_age=7 * 24 * 60 * 60,  # 7 days
            path='/'
        )
        
        return {
            'success': True,
            'user': {
                'id': user_id,
                'email': user_data['email'],
                'name': user_data['name'],
                'picture': user_data.get('picture'),
                'subscription_plan': 'free'
            }
        }
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f'Failed to connect to auth service: {str(e)}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Authentication failed: {str(e)}')

@router.get('/session/me')
async def get_session_user(request: Request):
    """Get current user from session cookie"""
    try:
        # Try to get session_token from cookie
        session_token = request.cookies.get('session_token')
        
        # Fallback to Authorization header
        if not session_token:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                session_token = auth_header.split(' ')[1]
        
        if not session_token:
            raise HTTPException(status_code=401, detail='Not authenticated')
        
        # Find session in database
        session = await db.user_sessions.find_one({'session_token': session_token})
        
        if not session:
            raise HTTPException(status_code=401, detail='Invalid session')
        
        # Check if session expired
        expires_at = session['expires_at']
        if expires_at.tzinfo is None:
            # If stored as naive datetime, assume UTC
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        if expires_at < datetime.now(timezone.utc):
            await db.user_sessions.delete_one({'session_token': session_token})
            raise HTTPException(status_code=401, detail='Session expired')
        
        # Get user data
        user = await db.users.find_one({'id': session['user_id']})
        if not user:
            # Fallback to _id
            user = await db.users.find_one({'_id': session['user_id']})
        
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        
        return {
            'id': user.get('id') or str(user['_id']),
            'email': user['email'],
            'name': user['name'],
            'picture': user.get('picture'),
            'subscription_plan': user.get('subscription_plan', 'free'),
            'videos_created': user.get('videos_created', 0),
            'created_at': user.get('created_at')
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to get user: {str(e)}')

@router.post('/logout')
async def logout(request: Request, response: Response):
    """Logout user and clear session"""
    try:
        # Get session_token from cookie
        session_token = request.cookies.get('session_token')
        
        if session_token:
            # Delete session from database
            await db.user_sessions.delete_one({'session_token': session_token})
        
        # Clear cookie
        response.delete_cookie(key='session_token', path='/')
        
        return {'success': True, 'message': 'Logged out successfully'}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Logout failed: {str(e)}')


# Password Reset Models
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post('/forgot-password')
async def forgot_password(request: ForgotPasswordRequest):
    """Request password reset - generates a token"""
    try:
        # Find user by email
        user = await db.users.find_one({'email': request.email})
        
        if not user:
            # Don't reveal if email exists for security
            return {
                'success': True,
                'message': 'If your email is registered, you will receive a password reset link'
            }
        
        # Generate reset token (using JWT with 15 min expiry)
        reset_token = create_access_token(
            data={'sub': request.email, 'type': 'password_reset'},
            expires_delta=timedelta(minutes=15)
        )
        
        # Store reset token in database with expiry
        reset_doc = {
            'email': request.email,
            'token': reset_token,
            'used': False,
            'created_at': datetime.now(timezone.utc),
            'expires_at': datetime.now(timezone.utc) + timedelta(minutes=15)
        }
        await db.password_resets.insert_one(reset_doc)
        
        # In a real app, send email with reset link
        # For now, return the token (in production, this should be sent via email)
        return {
            'success': True,
            'message': 'Password reset link sent to your email',
            'reset_token': reset_token  # Remove this in production!
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to process request: {str(e)}')

@router.post('/reset-password')
async def reset_password(request: ResetPasswordRequest):
    """Reset password using token"""
    try:
        # Verify token
        payload = decode_access_token(request.token)
        
        if not payload or payload.get('type') != 'password_reset':
            raise HTTPException(status_code=400, detail='Invalid or expired reset token')
        
        email = payload.get('sub')
        
        # Check if token exists in database and is not used
        reset_doc = await db.password_resets.find_one({
            'email': email,
            'token': request.token,
            'used': False
        })
        
        if not reset_doc:
            raise HTTPException(status_code=400, detail='Invalid or already used reset token')
        
        # Check if token expired
        expires_at = reset_doc['expires_at']
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail='Reset token has expired')
        
        # Validate new password
        if len(request.new_password) < 6:
            raise HTTPException(status_code=400, detail='Password must be at least 6 characters')
        
        # Update user password
        hashed_password = hash_password(request.new_password)
        result = await db.users.update_one(
            {'email': email},
            {
                '$set': {
                    'password': hashed_password,
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail='User not found')
        
        # Mark token as used
        await db.password_resets.update_one(
            {'token': request.token},
            {'$set': {'used': True}}
        )
        
        return {
            'success': True,
            'message': 'Password reset successfully'
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to reset password: {str(e)}')
