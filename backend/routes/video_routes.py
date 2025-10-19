from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
from bson import ObjectId
from services.video_ai_service import generate_script, search_stock_footage, generate_voiceover
from routes.auth_routes import get_current_user

router = APIRouter()

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Pydantic models
class VideoGenerationRequest(BaseModel):
    prompt: str
    video_length: str = "short"  # short, medium, long
    voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    include_voiceover: bool = True

class ScriptGenerationRequest(BaseModel):
    prompt: str
    video_length: str = "short"

@router.post('/generate-script')
async def create_script(request: ScriptGenerationRequest, current_user = Depends(get_current_user)):
    \"\"\"Generate AI script from prompt\"\"\"
    try:
        result = await generate_script(request.prompt, request.video_length)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error', 'Script generation failed'))
        
        return {
            'success': True,
            'script': result['script'],
            'scenes': result['scenes'],
            'word_count': result['word_count']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/generate-video')
async def create_video(request: VideoGenerationRequest, current_user = Depends(get_current_user)):
    \"\"\"Generate complete video from prompt\"\"\"
    try:
        # Step 1: Generate script
        script_result = await generate_script(request.prompt, request.video_length)
        
        if not script_result['success']:
            raise HTTPException(status_code=500, detail='Script generation failed')
        
        script_text = script_result['script']
        scenes = script_result['scenes']
        
        # Step 2: Find stock footage for each scene
        video_scenes = []
        for i, scene in enumerate(scenes):
            # Extract keywords from scene text for better search
            keywords = extract_keywords(scene['text'])
            footage = await search_stock_footage(keywords, count=1)
            
            video_scenes.append({
                'scene_number': i + 1,
                'text': scene['text'],
                'duration': scene['duration'],
                'footage': footage[0] if footage else None
            })
        
        # Step 3: Generate voiceover if requested
        voiceover_data = None
        if request.include_voiceover:
            voiceover_result = await generate_voiceover(script_text, request.voice)
            if voiceover_result['success']:
                voiceover_data = {
                    'filename': voiceover_result['filename'],
                    'path': voiceover_result['audio_path']
                }
        
        # Step 4: Save video to database
        video_data = {
            'user_id': str(current_user['_id']),
            'title': request.prompt[:100],
            'prompt': request.prompt,
            'script': script_text,
            'scenes': video_scenes,
            'voiceover': voiceover_data,
            'video_length': request.video_length,
            'status': 'completed',
            'created_at': datetime.utcnow().isoformat(),
            'views': 0
        }
        
        result = await db.videos.insert_one(video_data)
        
        # Update user's video count
        await db.users.update_one(
            {'_id': current_user['_id']},
            {'$inc': {'videos_created': 1}}
        )
        
        return {
            'success': True,
            'video_id': str(result.inserted_id),
            'script': script_text,
            'scenes': video_scenes,
            'voiceover': voiceover_data,
            'message': 'Video generated successfully!'
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/my-videos')
async def get_user_videos(current_user = Depends(get_current_user)):
    \"\"\"Get all videos created by current user\"\"\"
    videos = []
    cursor = db.videos.find({'user_id': str(current_user['_id'])}).sort('created_at', -1).limit(50)
    
    async for video in cursor:
        videos.append({
            'id': str(video['_id']),
            'title': video.get('title'),
            'prompt': video.get('prompt'),
            'status': video.get('status'),
            'created_at': video.get('created_at'),
            'thumbnail': video.get('scenes', [{}])[0].get('footage', {}).get('thumbnail') if video.get('scenes') else None
        })
    
    return {
        'success': True,
        'videos': videos,
        'total': len(videos)
    }

@router.get('/video/{video_id}')
async def get_video(video_id: str, current_user = Depends(get_current_user)):
    \"\"\"Get specific video details\"\"\"
    try:
        video = await db.videos.find_one({'_id': ObjectId(video_id), 'user_id': str(current_user['_id'])})
        
        if not video:
            raise HTTPException(status_code=404, detail='Video not found')
        
        return {
            'success': True,
            'video': {
                'id': str(video['_id']),
                'title': video.get('title'),
                'prompt': video.get('prompt'),
                'script': video.get('script'),
                'scenes': video.get('scenes'),
                'voiceover': video.get('voiceover'),
                'status': video.get('status'),
                'created_at': video.get('created_at')
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/video/{video_id}')
async def delete_video(video_id: str, current_user = Depends(get_current_user)):
    \"\"\"Delete a video\"\"\"
    try:
        result = await db.videos.delete_one({'_id': ObjectId(video_id), 'user_id': str(current_user['_id'])})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail='Video not found')
        
        return {
            'success': True,
            'message': 'Video deleted successfully'
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_keywords(text: str) -> str:
    \"\"\"Extract main keywords from text for stock footage search\"\"\"
    # Simple keyword extraction - take first few words or main nouns
    words = text.split()[:5]
    # Remove common words
    stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for'}
    keywords = [word for word in words if word.lower() not in stop_words]
    return ' '.join(keywords[:3])
