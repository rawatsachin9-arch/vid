#!/usr/bin/env python3
"""
Backend API Testing for AI Video Generation with Image URL Fix
Focus: Testing that images are stored as URLs instead of base64 to avoid MongoDB 16MB limit
"""

import asyncio
import httpx
import json
import time
import os
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient

# Configuration - Use external URL from frontend/.env
BACKEND_URL = "https://c-project-4.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database"

# Test data - specific prompt from review request
TEST_VIDEO_DATA = {
    "title": "Elephants in Savannah",
    "input_text": "Elephants playing in the savannah"
}

class BackendTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=180.0)  # 3 minute timeout for AI generation
        self.mongo_client = MongoClient(MONGO_URL)
        self.db = self.mongo_client[DB_NAME]
        self.session_token = None
        self.user_id = None
        self.project_id = None
        
    async def setup_test_user(self):
        """Create test user and session for authentication"""
        print("🔧 Setting up test user and session...")
        
        # Generate unique identifiers
        timestamp = int(time.time())
        self.user_id = f"test-user-{timestamp}"
        self.session_token = f"test_session_{timestamp}"
        
        # Create test user
        user_doc = {
            'id': self.user_id,
            'email': f'test.user.{timestamp}@example.com',
            'name': 'Test User AI Video',
            'picture': 'https://via.placeholder.com/150',
            'subscription_plan': 'free',
            'videos_created': 0,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'updated_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Create session
        session_doc = {
            'user_id': self.user_id,
            'session_token': self.session_token,
            'expires_at': datetime.now(timezone.utc) + timedelta(days=7),
            'created_at': datetime.now(timezone.utc)
        }
        
        try:
            self.db.users.insert_one(user_doc)
            self.db.user_sessions.insert_one(session_doc)
            print(f"✅ Created test user: {self.user_id}")
            print(f"✅ Created session token: {self.session_token}")
        except Exception as e:
            print(f"❌ Failed to create test user: {e}")
            raise
    
    async def test_auth_session_me(self):
        """Test GET /api/auth/session/me endpoint"""
        print("\n🔐 Testing Authentication - GET /api/auth/session/me")
        
        try:
            response = await self.client.get(
                f"{API_BASE}/auth/session/me",
                headers={"Authorization": f"Bearer {self.session_token}"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ Authentication successful")
                print(f"   User ID: {user_data.get('id')}")
                print(f"   Email: {user_data.get('email')}")
                print(f"   Name: {user_data.get('name')}")
                return True
            else:
                print(f"❌ Authentication failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Auth test error: {e}")
            return False
    
    async def test_google_oauth_session(self):
        """Test POST /api/auth/google/session endpoint"""
        print("\n🔐 Testing Google OAuth Session - POST /api/auth/google/session")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/google/session",
                headers={"X-Session-ID": self.session_token}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Google OAuth session processed successfully")
                print(f"   Success: {result.get('success')}")
                return True
            else:
                print(f"❌ Google OAuth session failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Google OAuth test error: {e}")
            return False
    
    async def test_logout(self):
        """Test POST /api/auth/logout endpoint"""
        print("\n🔐 Testing Logout - POST /api/auth/logout")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/logout",
                cookies={"session_token": self.session_token}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Logout successful: {result.get('message')}")
                return True
            else:
                print(f"❌ Logout failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Logout test error: {e}")
            return False
    
    async def test_video_generation(self):
        """Test POST /api/video/generate endpoint"""
        print("\n🎬 Testing AI Video Generation - POST /api/video/generate")
        print(f"   Title: {TEST_VIDEO_DATA['title']}")
        print(f"   Input: {TEST_VIDEO_DATA['input_text']}")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/video/generate",
                json=TEST_VIDEO_DATA,
                headers={"Authorization": f"Bearer {self.session_token}"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                project = response.json()
                self.project_id = project['id']
                print(f"✅ Video project created successfully")
                print(f"   Project ID: {project['id']}")
                print(f"   Status: {project['status']}")
                print(f"   Title: {project['title']}")
                return True
            else:
                print(f"❌ Video generation failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Video generation test error: {e}")
            return False
    
    async def test_project_status_polling(self):
        """Test GET /api/video/projects/{id} with status polling"""
        if not self.project_id:
            print("❌ No project ID available for polling")
            return False
            
        print(f"\n📊 Testing Project Status Polling - GET /api/video/projects/{self.project_id}")
        print("   Polling every 3 seconds until completion or timeout (120s)...")
        
        start_time = time.time()
        timeout = 120  # 2 minutes timeout
        
        try:
            while time.time() - start_time < timeout:
                response = await self.client.get(
                    f"{API_BASE}/video/projects/{self.project_id}",
                    headers={"Authorization": f"Bearer {self.session_token}"}
                )
                
                if response.status_code != 200:
                    print(f"❌ Failed to get project status: {response.text}")
                    return False
                
                project = response.json()
                status = project['status']
                elapsed = int(time.time() - start_time)
                
                print(f"   [{elapsed}s] Status: {status}")
                
                if status == 'completed':
                    print(f"✅ Video generation completed successfully!")
                    print(f"   Scenes generated: {len(project.get('scenes', []))}")
                    print(f"   Duration: {project.get('duration', 0)} seconds")
                    print(f"   Thumbnail URL: {'✅ Set' if project.get('thumbnail_url') else '❌ Not set'}")
                    
                    # Verify scenes have images
                    scenes = project.get('scenes', [])
                    scenes_with_images = sum(1 for scene in scenes if scene.get('image_url'))
                    print(f"   Scenes with images: {scenes_with_images}/{len(scenes)}")
                    
                    # Check scene structure
                    if scenes:
                        scene = scenes[0]
                        print(f"   Sample scene structure:")
                        print(f"     - Scene number: {scene.get('scene_number')}")
                        print(f"     - Description: {scene.get('description', '')[:50]}...")
                        print(f"     - Narration: {scene.get('narration', '')[:50]}...")
                        print(f"     - Image prompt: {scene.get('image_prompt', '')[:50]}...")
                        print(f"     - Image URL: {'✅ Base64 data' if scene.get('image_url', '').startswith('data:image') else '❌ Missing'}")
                    
                    return True
                    
                elif status == 'failed':
                    error_msg = project.get('error_message', 'Unknown error')
                    print(f"❌ Video generation failed: {error_msg}")
                    return False
                
                # Wait before next poll
                await asyncio.sleep(3)
            
            print(f"❌ Timeout reached ({timeout}s) - video generation did not complete")
            return False
            
        except Exception as e:
            print(f"❌ Project polling error: {e}")
            return False
    
    async def test_get_all_projects(self):
        """Test GET /api/video/projects endpoint"""
        print("\n📋 Testing Get All Projects - GET /api/video/projects")
        
        try:
            response = await self.client.get(
                f"{API_BASE}/video/projects",
                headers={"Authorization": f"Bearer {self.session_token}"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                projects = response.json()
                print(f"✅ Retrieved {len(projects)} projects")
                
                if projects:
                    project = projects[0]
                    print(f"   Latest project:")
                    print(f"     - ID: {project['id']}")
                    print(f"     - Title: {project['title']}")
                    print(f"     - Status: {project['status']}")
                    print(f"     - Scenes: {len(project.get('scenes', []))}")
                
                return True
            else:
                print(f"❌ Failed to get projects: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Get projects test error: {e}")
            return False
    
    async def test_delete_project(self):
        """Test DELETE /api/video/projects/{id} endpoint"""
        if not self.project_id:
            print("❌ No project ID available for deletion")
            return False
            
        print(f"\n🗑️ Testing Delete Project - DELETE /api/video/projects/{self.project_id}")
        
        try:
            response = await self.client.delete(
                f"{API_BASE}/video/projects/{self.project_id}",
                headers={"Authorization": f"Bearer {self.session_token}"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Project deleted successfully: {result.get('message')}")
                return True
            else:
                print(f"❌ Failed to delete project: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Delete project test error: {e}")
            return False
    
    async def cleanup_test_data(self):
        """Clean up test user and session data"""
        print("\n🧹 Cleaning up test data...")
        
        try:
            # Delete test user and session
            self.db.users.delete_many({'id': self.user_id})
            self.db.user_sessions.delete_many({'user_id': self.user_id})
            self.db.video_projects.delete_many({'user_id': self.user_id})
            print("✅ Test data cleaned up")
        except Exception as e:
            print(f"❌ Cleanup error: {e}")
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_backend_tests():
    """Run all backend tests"""
    print("🚀 Starting Backend API Tests for AI Video Generation Platform")
    print("=" * 70)
    
    tester = BackendTester()
    test_results = {}
    
    try:
        # Setup
        await tester.setup_test_user()
        
        # Authentication Tests
        test_results['auth_session_me'] = await tester.test_auth_session_me()
        test_results['google_oauth_session'] = await tester.test_google_oauth_session()
        
        # AI Video Generation Tests
        test_results['video_generation'] = await tester.test_video_generation()
        test_results['project_status_polling'] = await tester.test_project_status_polling()
        
        # Video Projects CRUD Tests
        test_results['get_all_projects'] = await tester.test_get_all_projects()
        test_results['delete_project'] = await tester.test_delete_project()
        
        # Auth Tests (continued)
        test_results['logout'] = await tester.test_logout()
        
    except Exception as e:
        print(f"\n❌ Critical test error: {e}")
    
    finally:
        await tester.cleanup_test_data()
        await tester.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the detailed output above.")
    
    return test_results

if __name__ == "__main__":
    asyncio.run(run_backend_tests())