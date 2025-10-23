#!/usr/bin/env python3
"""
Quick Backend API Test for AI Video Generation
"""

import asyncio
import httpx
import json
import time
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

# Configuration
API_BASE = "http://localhost:8001/api"
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database"

class QuickTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.mongo_client = MongoClient(MONGO_URL)
        self.db = self.mongo_client[DB_NAME]
        self.session_token = None
        self.user_id = None
        
    async def setup_test_user(self):
        """Create test user and session"""
        timestamp = int(time.time())
        self.user_id = f"test-user-{timestamp}"
        self.session_token = f"test_session_{timestamp}"
        
        # Create test user
        user_doc = {
            'id': self.user_id,
            'email': f'test.user.{timestamp}@example.com',
            'name': 'Test User AI Video',
            'subscription_plan': 'free',
            'videos_created': 0,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Create session
        session_doc = {
            'user_id': self.user_id,
            'session_token': self.session_token,
            'expires_at': datetime.now(timezone.utc) + timedelta(days=7),
            'created_at': datetime.now(timezone.utc)
        }
        
        self.db.users.insert_one(user_doc)
        self.db.user_sessions.insert_one(session_doc)
        print(f"✅ Created test user: {self.user_id}")
        print(f"✅ Session token: {self.session_token}")
    
    async def test_auth(self):
        """Test authentication"""
        print("\n🔐 Testing Authentication")
        response = await self.client.get(
            f"{API_BASE}/auth/session/me",
            headers={"Authorization": f"Bearer {self.session_token}"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Auth successful - User: {user_data['name']}")
            return True
        else:
            print(f"❌ Auth failed: {response.text}")
            return False
    
    async def test_video_generation_start(self):
        """Test starting video generation"""
        print("\n🎬 Testing Video Generation Start")
        
        video_data = {
            "title": "AI Test Video",
            "input_text": "Create a short video about artificial intelligence."
        }
        
        response = await self.client.post(
            f"{API_BASE}/video/generate",
            json=video_data,
            headers={"Authorization": f"Bearer {self.session_token}"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            project = response.json()
            print(f"✅ Video project created: {project['id']}")
            print(f"   Status: {project['status']}")
            return project['id']
        else:
            print(f"❌ Video generation failed: {response.text}")
            return None
    
    async def test_project_status(self, project_id):
        """Test getting project status"""
        print(f"\n📊 Testing Project Status: {project_id}")
        
        response = await self.client.get(
            f"{API_BASE}/video/projects/{project_id}",
            headers={"Authorization": f"Bearer {self.session_token}"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            project = response.json()
            print(f"✅ Project status: {project['status']}")
            print(f"   Scenes: {len(project.get('scenes', []))}")
            return True
        else:
            print(f"❌ Failed to get project: {response.text}")
            return False
    
    async def test_get_projects(self):
        """Test getting all projects"""
        print("\n📋 Testing Get All Projects")
        
        response = await self.client.get(
            f"{API_BASE}/video/projects",
            headers={"Authorization": f"Bearer {self.session_token}"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Retrieved {len(projects)} projects")
            return True
        else:
            print(f"❌ Failed to get projects: {response.text}")
            return False
    
    async def cleanup(self):
        """Clean up test data"""
        self.db.users.delete_many({'id': self.user_id})
        self.db.user_sessions.delete_many({'user_id': self.user_id})
        self.db.video_projects.delete_many({'user_id': self.user_id})
        await self.client.aclose()
        print("✅ Cleanup completed")

async def main():
    print("🚀 Quick Backend API Test")
    print("=" * 50)
    
    tester = QuickTester()
    
    try:
        await tester.setup_test_user()
        
        # Test authentication
        auth_ok = await tester.test_auth()
        if not auth_ok:
            return
        
        # Test video generation
        project_id = await tester.test_video_generation_start()
        if project_id:
            await tester.test_project_status(project_id)
        
        # Test get all projects
        await tester.test_get_projects()
        
    finally:
        await tester.cleanup()

if __name__ == "__main__":
    asyncio.run(main())