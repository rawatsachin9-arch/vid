from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from models.video_project import VideoProject, VideoProjectCreate, VideoProjectResponse, VideoStatus, Scene
from services.ai_video_service import AIVideoService
from utils.auth import get_current_user_from_token
import uuid

router = APIRouter(prefix="/api/video", tags=["video"])

# MongoDB connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "test_database")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

ai_video_service = AIVideoService()

@router.post("/generate", response_model=VideoProjectResponse)
async def create_video_project(
    project: VideoProjectCreate,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Create a new video project and start AI generation
    """
    try:
        # Create project ID
        project_id = str(uuid.uuid4())
        
        # Create project document
        video_project = {
            "_id": project_id,
            "user_id": current_user["id"],
            "title": project.title,
            "input_text": project.input_text,
            "status": VideoStatus.PENDING,
            "scenes": [],
            "video_url": None,
            "thumbnail_url": None,
            "duration": 0,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "error_message": None
        }
        
        # Insert into database
        await db.video_projects.insert_one(video_project)
        
        # Start background task for video generation
        background_tasks.add_task(generate_video_background, project_id, project.input_text)
        
        return VideoProjectResponse(
            id=project_id,
            user_id=current_user["id"],
            title=project.title,
            status=VideoStatus.PENDING,
            scenes=[],
            video_url=None,
            thumbnail_url=None,
            duration=0,
            created_at=video_project["created_at"],
            updated_at=video_project["updated_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create video project: {str(e)}")

async def generate_video_background(project_id: str, input_text: str):
    """
    Background task to generate video scenes and images
    """
    # Create async MongoDB client for background task
    bg_client = AsyncIOMotorClient(MONGO_URL)
    bg_db = bg_client[DB_NAME]
    
    try:
        # Update status to processing
        await bg_db.video_projects.update_one(
            {"_id": project_id},
            {"$set": {"status": VideoStatus.PROCESSING, "updated_at": datetime.now()}}
        )
        
        # Generate script and scenes  
        await bg_db.video_projects.update_one(
            {"_id": project_id},
            {"$set": {"status": VideoStatus.GENERATING_SCRIPT, "updated_at": datetime.now()}}
        )
        
        scenes = await ai_video_service.generate_script_scenes(input_text)
        
        # Save scenes to database
        await bg_db.video_projects.update_one(
            {"_id": project_id},
            {"$set": {"scenes": scenes, "updated_at": datetime.now()}}
        )
        
        # Generate images for scenes
        await bg_db.video_projects.update_one(
            {"_id": project_id},
            {"$set": {"status": VideoStatus.GENERATING_IMAGES, "updated_at": datetime.now()}}
        )
        
        scenes_with_images = await ai_video_service.generate_all_scene_images(scenes)
        
        # Calculate total duration
        total_duration = sum(scene.get('duration', 5) for scene in scenes_with_images)
        
        # Set thumbnail as first scene image
        thumbnail_url = scenes_with_images[0].get('image_url') if scenes_with_images else None
        
        # Update project with completed status
        await bg_db.video_projects.update_one(
            {"_id": project_id},
            {
                "$set": {
                    "status": VideoStatus.COMPLETED,
                    "scenes": scenes_with_images,
                    "duration": total_duration,
                    "thumbnail_url": thumbnail_url,
                    "updated_at": datetime.now()
                }
            }
        )
        
    except Exception as e:
        print(f"Error in background video generation: {e}")
        await bg_db.video_projects.update_one(
            {"_id": project_id},
            {
                "$set": {
                    "status": VideoStatus.FAILED,
                    "error_message": str(e),
                    "updated_at": datetime.now()
                }
            }
        )
    finally:
        bg_client.close()

@router.get("/projects", response_model=List[VideoProjectResponse])
async def get_user_projects(current_user: dict = Depends(get_current_user_from_token)):
    """
    Get all video projects for the current user
    """
    try:
        projects = await db.video_projects.find({"user_id": current_user["id"]}).sort("created_at", -1).to_list(1000)
        
        return [
            VideoProjectResponse(
                id=p["_id"],
                user_id=p["user_id"],
                title=p["title"],
                status=p["status"],
                scenes=[Scene(**s) for s in p.get("scenes", [])],
                video_url=p.get("video_url"),
                thumbnail_url=p.get("thumbnail_url"),
                duration=p.get("duration", 0),
                created_at=p["created_at"],
                updated_at=p["updated_at"],
                error_message=p.get("error_message")
            )
            for p in projects
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch projects: {str(e)}")

@router.get("/projects/{project_id}", response_model=VideoProjectResponse)
async def get_project(project_id: str, current_user: dict = Depends(get_current_user_from_token)):
    """
    Get a specific video project
    """
    try:
        project = await db.video_projects.find_one({"_id": project_id, "user_id": current_user["id"]})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return VideoProjectResponse(
            id=project["_id"],
            user_id=project["user_id"],
            title=project["title"],
            status=project["status"],
            scenes=[Scene(**s) for s in project.get("scenes", [])],
            video_url=project.get("video_url"),
            thumbnail_url=project.get("thumbnail_url"),
            duration=project.get("duration", 0),
            created_at=project["created_at"],
            updated_at=project["updated_at"],
            error_message=project.get("error_message")
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch project: {str(e)}")

@router.delete("/projects/{project_id}")
async def delete_project(project_id: str, current_user: dict = Depends(get_current_user_from_token)):
    """
    Delete a video project
    """
    try:
        result = await db.video_projects.delete_one({"_id": project_id, "user_id": current_user["id"]})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"message": "Project deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")
