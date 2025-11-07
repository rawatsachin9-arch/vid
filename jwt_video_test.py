#!/usr/bin/env python3
"""
JWT-based AI Video Generation Testing
Tests the complete video generation flow with JWT authentication
"""

import asyncio
import httpx
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "Test123!"

# Test video data
TEST_VIDEO_DATA = {
    "title": "Test Video",
    "input_text": "Create a short video about AI technology transforming the world"
}

class JWTVideoTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=180.0)
        self.access_token = None
        self.project_id = None
        
    async def test_login(self):
        """Test 1: Login to get access token"""
        print("\n" + "="*70)
        print("TEST 1: JWT Authentication - POST /api/auth/login")
        print("="*70)
        print(f"📧 Email: {TEST_EMAIL}")
        print(f"🔒 Password: {TEST_PASSWORD}")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD
                }
            )
            
            print(f"\n📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                user = data.get('user', {})
                
                print(f"✅ LOGIN SUCCESSFUL")
                print(f"\n🎫 Access Token: {self.access_token[:50]}...")
                print(f"\n👤 User Information:")
                print(f"   - ID: {user.get('id')}")
                print(f"   - Email: {user.get('email')}")
                print(f"   - Name: {user.get('name')}")
                print(f"   - Subscription: {user.get('subscription_plan')}")
                print(f"   - Token Type: {data.get('token_type')}")
                return True
            else:
                print(f"❌ LOGIN FAILED")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ LOGIN ERROR: {e}")
            return False
    
    async def test_create_video_project(self):
        """Test 2: Create a video project with Bearer token"""
        print("\n" + "="*70)
        print("TEST 2: Create Video Project - POST /api/video/generate")
        print("="*70)
        print(f"🎬 Title: {TEST_VIDEO_DATA['title']}")
        print(f"📝 Input Text: {TEST_VIDEO_DATA['input_text']}")
        print(f"🔑 Using Bearer Token Authentication")
        
        if not self.access_token:
            print("❌ No access token available. Login first.")
            return False
        
        try:
            response = await self.client.post(
                f"{API_BASE}/video/generate",
                json=TEST_VIDEO_DATA,
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"\n📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                project = response.json()
                self.project_id = project.get('id')
                
                print(f"✅ VIDEO PROJECT CREATED SUCCESSFULLY")
                print(f"\n📋 Project Details:")
                print(f"   - Project ID: {self.project_id}")
                print(f"   - Title: {project.get('title')}")
                print(f"   - Status: {project.get('status')}")
                print(f"   - User ID: {project.get('user_id')}")
                print(f"   - Created At: {project.get('created_at')}")
                
                if project.get('status') == 'pending':
                    print(f"\n✅ Status is 'pending' - Background processing started")
                else:
                    print(f"\n⚠️  Expected status 'pending', got '{project.get('status')}'")
                
                return True
            else:
                print(f"❌ VIDEO PROJECT CREATION FAILED")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ VIDEO PROJECT CREATION ERROR: {e}")
            return False
    
    async def test_check_project_status(self):
        """Test 3: Check project status after 5 seconds"""
        print("\n" + "="*70)
        print("TEST 3: Check Project Status - GET /api/video/projects/{project_id}")
        print("="*70)
        
        if not self.project_id:
            print("❌ No project ID available. Create a project first.")
            return False
        
        print(f"⏳ Waiting 5 seconds before checking status...")
        await asyncio.sleep(5)
        
        try:
            response = await self.client.get(
                f"{API_BASE}/video/projects/{self.project_id}",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"\n📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                project = response.json()
                
                print(f"✅ PROJECT STATUS RETRIEVED SUCCESSFULLY")
                print(f"\n📋 Project Status:")
                print(f"   - Project ID: {project.get('id')}")
                print(f"   - Title: {project.get('title')}")
                print(f"   - Status: {project.get('status')}")
                print(f"   - Duration: {project.get('duration')} seconds")
                print(f"   - Scenes: {len(project.get('scenes', []))} scenes")
                print(f"   - Thumbnail URL: {'✅ Set' if project.get('thumbnail_url') else '❌ Not set'}")
                print(f"   - Updated At: {project.get('updated_at')}")
                
                if project.get('error_message'):
                    print(f"   - Error: {project.get('error_message')}")
                
                # Show scene details if available
                scenes = project.get('scenes', [])
                if scenes:
                    print(f"\n🎬 Scene Details:")
                    for i, scene in enumerate(scenes[:3], 1):  # Show first 3 scenes
                        print(f"   Scene {i}:")
                        print(f"     - Number: {scene.get('scene_number')}")
                        print(f"     - Description: {scene.get('description', '')[:60]}...")
                        print(f"     - Narration: {scene.get('narration', '')[:60]}...")
                        print(f"     - Image: {'✅ Generated' if scene.get('image_url') else '❌ Not generated'}")
                    
                    if len(scenes) > 3:
                        print(f"   ... and {len(scenes) - 3} more scenes")
                
                return True
            else:
                print(f"❌ FAILED TO GET PROJECT STATUS")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ PROJECT STATUS CHECK ERROR: {e}")
            return False
    
    async def test_list_all_projects(self):
        """Test 4: List all projects"""
        print("\n" + "="*70)
        print("TEST 4: List All Projects - GET /api/video/projects")
        print("="*70)
        
        try:
            response = await self.client.get(
                f"{API_BASE}/video/projects",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"\n📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                projects = response.json()
                
                print(f"✅ PROJECTS LIST RETRIEVED SUCCESSFULLY")
                print(f"\n📋 Total Projects: {len(projects)}")
                
                if projects:
                    print(f"\n🎬 Projects Summary:")
                    for i, project in enumerate(projects[:5], 1):  # Show first 5 projects
                        print(f"\n   Project {i}:")
                        print(f"     - ID: {project.get('id')}")
                        print(f"     - Title: {project.get('title')}")
                        print(f"     - Status: {project.get('status')}")
                        print(f"     - Scenes: {len(project.get('scenes', []))}")
                        print(f"     - Duration: {project.get('duration')} seconds")
                        print(f"     - Created: {project.get('created_at')}")
                    
                    if len(projects) > 5:
                        print(f"\n   ... and {len(projects) - 5} more projects")
                else:
                    print(f"\n⚠️  No projects found for this user")
                
                return True
            else:
                print(f"❌ FAILED TO GET PROJECTS LIST")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ PROJECTS LIST ERROR: {e}")
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_jwt_video_tests():
    """Run all JWT video generation tests"""
    print("\n" + "="*70)
    print("🚀 AI VIDEO GENERATION SYSTEM - JWT AUTHENTICATION TESTING")
    print("="*70)
    print(f"⏰ Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = JWTVideoTester()
    test_results = {}
    
    try:
        # Test 1: Login
        test_results['login'] = await tester.test_login()
        
        if not test_results['login']:
            print("\n❌ Login failed. Cannot proceed with other tests.")
            return test_results
        
        # Test 2: Create video project
        test_results['create_project'] = await tester.test_create_video_project()
        
        # Test 3: Check project status (after 5 seconds)
        test_results['check_status'] = await tester.test_check_project_status()
        
        # Test 4: List all projects
        test_results['list_projects'] = await tester.test_list_all_projects()
        
    except Exception as e:
        print(f"\n❌ Critical test error: {e}")
    
    finally:
        await tester.close()
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST RESULTS SUMMARY")
    print("="*70)
    
    test_names = {
        'login': 'JWT Login Authentication',
        'create_project': 'Create Video Project',
        'check_status': 'Check Project Status',
        'list_projects': 'List All Projects'
    }
    
    passed = 0
    total = len(test_results)
    
    for test_key, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        test_name = test_names.get(test_key, test_key)
        print(f"{test_name:<35} {status}")
        if result:
            passed += 1
    
    print(f"\n{'='*70}")
    print(f"Overall Result: {passed}/{total} tests passed")
    print(f"⏰ Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! AI Video Generation System is working correctly.")
    else:
        print("⚠️  SOME TESTS FAILED. Check the detailed output above.")
    
    print("="*70)
    
    return test_results

if __name__ == "__main__":
    asyncio.run(run_jwt_video_tests())
