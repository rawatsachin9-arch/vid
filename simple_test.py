#!/usr/bin/env python3
"""
Simple Backend Test - Just check if APIs are working
"""

import asyncio
import httpx
import time
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

async def test_backend():
    print("🚀 Simple Backend Test")
    
    # Setup
    mongo_client = MongoClient('mongodb://localhost:27017')
    db = mongo_client['test_database']
    
    timestamp = int(time.time())
    user_id = f"test-user-{timestamp}"
    session_token = f"test_session_{timestamp}"
    
    # Create test user and session
    user_doc = {
        'id': user_id,
        'email': f'test.user.{timestamp}@example.com',
        'name': 'Test User',
        'subscription_plan': 'free',
        'videos_created': 0,
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    
    session_doc = {
        'user_id': user_id,
        'session_token': session_token,
        'expires_at': datetime.now(timezone.utc) + timedelta(days=7),
        'created_at': datetime.now(timezone.utc)
    }
    
    db.users.insert_one(user_doc)
    db.user_sessions.insert_one(session_doc)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Test 1: Authentication
        print("\n1. Testing Authentication...")
        response = await client.get(
            "http://localhost:8001/api/auth/session/me",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Authentication working")
        else:
            print(f"   ❌ Auth failed: {response.text}")
            return
        
        # Test 2: Video Generation Start
        print("\n2. Testing Video Generation Start...")
        video_data = {
            "title": "Test AI Video",
            "input_text": "Create a short video about artificial intelligence."
        }
        
        response = await client.post(
            "http://localhost:8001/api/video/generate",
            json=video_data,
            headers={"Authorization": f"Bearer {session_token}"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            project = response.json()
            project_id = project['id']
            print(f"   ✅ Video project created: {project_id}")
            print(f"   Status: {project['status']}")
        else:
            print(f"   ❌ Video generation failed: {response.text}")
            return
        
        # Test 3: Get Project Status (immediate)
        print("\n3. Testing Get Project Status...")
        response = await client.get(
            f"http://localhost:8001/api/video/projects/{project_id}",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            project = response.json()
            print(f"   ✅ Project status: {project['status']}")
            print(f"   Scenes: {len(project.get('scenes', []))}")
        else:
            print(f"   ❌ Failed to get project: {response.text}")
        
        # Test 4: Get All Projects
        print("\n4. Testing Get All Projects...")
        response = await client.get(
            "http://localhost:8001/api/video/projects",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            print(f"   ✅ Retrieved {len(projects)} projects")
        else:
            print(f"   ❌ Failed to get projects: {response.text}")
        
        # Test 5: Google OAuth Session (will fail but should not crash)
        print("\n5. Testing Google OAuth Session...")
        response = await client.post(
            "http://localhost:8001/api/auth/google/session",
            headers={"X-Session-ID": session_token}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Google OAuth session processed")
        else:
            print(f"   ❌ Google OAuth failed (expected): {response.status_code}")
        
        # Test 6: Logout
        print("\n6. Testing Logout...")
        response = await client.post(
            "http://localhost:8001/api/auth/logout",
            cookies={"session_token": session_token}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Logout successful")
        else:
            print(f"   ❌ Logout failed: {response.text}")
    
    # Cleanup
    db.users.delete_many({'id': user_id})
    db.user_sessions.delete_many({'user_id': user_id})
    db.video_projects.delete_many({'user_id': user_id})
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    asyncio.run(test_backend())