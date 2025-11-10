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
BACKEND_URL = "https://core.preview.emergentagent.com"
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
        
    async def test_jwt_login(self):
        """Test JWT login with testuser@example.com as specified in review request"""
        print("🔐 Testing JWT Login with testuser@example.com")
        
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json=login_data
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.session_token = result.get('access_token')
                user_data = result.get('user', {})
                self.user_id = user_data.get('id')
                
                print(f"✅ JWT Login successful")
                print(f"   User ID: {self.user_id}")
                print(f"   Email: {user_data.get('email')}")
                print(f"   Name: {user_data.get('name')}")
                print(f"   Access Token: {self.session_token[:20]}...")
                return True
            else:
                print(f"❌ JWT Login failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ JWT Login error: {e}")
            return False
    
    # Removed session-based auth methods - using JWT authentication instead
    
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
        """Test GET /api/video/projects/{id} with focus on Image URL Fix"""
        if not self.project_id:
            print("❌ No project ID available for polling")
            return False
            
        print(f"\n📊 Testing Video Generation Progress - Focus: Image URL Fix")
        print(f"   Project ID: {self.project_id}")
        print("   Polling every 5 seconds until completion or timeout (120s)...")
        print("   Expected status progression: pending → processing → generating_script → generating_images → completed")
        
        start_time = time.time()
        timeout = 120  # 2 minutes timeout as specified in review request
        
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
                    
                    # Critical verification: Check for MongoDB "document too large" errors
                    if project.get('error_message'):
                        print(f"❌ Error message found: {project['error_message']}")
                        return False
                    else:
                        print(f"✅ No error messages - MongoDB document size issue resolved")
                    
                    # Verify scene structure
                    scenes = project.get('scenes', [])
                    print(f"   Scenes generated: {len(scenes)}")
                    
                    if not scenes:
                        print(f"❌ No scenes generated")
                        return False
                    
                    # Verify each scene has proper image URL (not base64, not placeholder)
                    valid_scenes = 0
                    for i, scene in enumerate(scenes):
                        image_url = scene.get('image_url', '')
                        
                        # Check if image_url is valid HTTP/HTTPS URL
                        is_valid_url = image_url.startswith('http://') or image_url.startswith('https://')
                        is_not_placeholder = 'placeholder' not in image_url.lower()
                        is_not_base64 = not image_url.startswith('data:')
                        
                        print(f"     Scene {i+1}:")
                        print(f"       - Description: {scene.get('description', '')[:50]}...")
                        print(f"       - Narration: {scene.get('narration', '')[:50]}...")
                        print(f"       - Duration: {scene.get('duration', 0)}s")
                        print(f"       - Image URL: {'✅ Valid HTTP/HTTPS' if is_valid_url else '❌ Invalid URL'}")
                        print(f"       - Not Placeholder: {'✅ Real image' if is_not_placeholder else '❌ Placeholder'}")
                        print(f"       - Not Base64: {'✅ URL format' if is_not_base64 else '❌ Base64 format'}")
                        
                        if is_valid_url and is_not_placeholder and is_not_base64:
                            valid_scenes += 1
                    
                    print(f"   Valid scenes with proper image URLs: {valid_scenes}/{len(scenes)}")
                    
                    # Check thumbnail URL
                    thumbnail_url = project.get('thumbnail_url', '')
                    if thumbnail_url:
                        is_valid_thumb = thumbnail_url.startswith('http://') or thumbnail_url.startswith('https://')
                        print(f"   Thumbnail URL: {'✅ Valid' if is_valid_thumb else '❌ Invalid'}")
                    
                    # Overall success criteria
                    if valid_scenes == len(scenes) and valid_scenes >= 3:
                        print(f"✅ IMAGE URL FIX VERIFIED: All scenes have valid HTTP/HTTPS image URLs")
                        return True
                    else:
                        print(f"❌ IMAGE URL FIX FAILED: {len(scenes) - valid_scenes} scenes have invalid URLs")
                        return False
                    
                elif status == 'failed':
                    error_msg = project.get('error_message', 'Unknown error')
                    print(f"❌ Video generation failed: {error_msg}")
                    
                    # Check if it's the MongoDB document size error we're trying to fix
                    if 'document too large' in error_msg.lower() or '16mb' in error_msg.lower():
                        print(f"❌ CRITICAL: MongoDB document size error still occurring!")
                    
                    return False
                
                # Wait before next poll (5 seconds as specified in review request)
                await asyncio.sleep(5)
            
            print(f"❌ Timeout reached ({timeout}s) - video generation did not complete")
            return False
            
        except Exception as e:
            print(f"❌ Project polling error: {e}")
            return False
    
    async def test_image_accessibility(self):
        """Test that generated image URLs are accessible via HTTP requests"""
        if not self.project_id:
            print("❌ No project ID available for image accessibility test")
            return False
            
        print(f"\n🖼️ Testing Image Accessibility - Verify Images Are Accessible")
        
        try:
            # Get the completed project
            response = await self.client.get(
                f"{API_BASE}/video/projects/{self.project_id}",
                headers={"Authorization": f"Bearer {self.session_token}"}
            )
            
            if response.status_code != 200:
                print(f"❌ Failed to get project: {response.text}")
                return False
            
            project = response.json()
            scenes = project.get('scenes', [])
            
            if not scenes:
                print(f"❌ No scenes to test")
                return False
            
            # Test accessibility of first 2 image URLs as specified in review request
            test_count = min(2, len(scenes))
            accessible_count = 0
            
            for i in range(test_count):
                scene = scenes[i]
                image_url = scene.get('image_url', '')
                
                if not image_url or not (image_url.startswith('http://') or image_url.startswith('https://')):
                    print(f"   Scene {i+1}: ❌ Invalid URL format: {image_url[:100]}")
                    continue
                
                print(f"   Scene {i+1}: Testing {image_url[:100]}...")
                
                try:
                    # Make HTTP GET request to verify image is accessible
                    img_response = await self.client.get(image_url, timeout=30.0)
                    
                    if img_response.status_code == 200:
                        content_type = img_response.headers.get('content-type', '')
                        content_length = len(img_response.content)
                        
                        print(f"     ✅ Image accessible (Status: 200)")
                        print(f"     ✅ Content-Type: {content_type}")
                        print(f"     ✅ Content-Length: {content_length} bytes")
                        
                        if 'image' in content_type.lower():
                            accessible_count += 1
                        else:
                            print(f"     ⚠️  Warning: Content-Type is not image format")
                    else:
                        print(f"     ❌ Image not accessible (Status: {img_response.status_code})")
                        
                except Exception as e:
                    print(f"     ❌ Error accessing image: {e}")
            
            print(f"   Accessible images: {accessible_count}/{test_count}")
            
            if accessible_count == test_count:
                print(f"✅ All tested images are accessible from their URLs")
                return True
            else:
                print(f"❌ {test_count - accessible_count} images are not accessible")
                return False
                
        except Exception as e:
            print(f"❌ Image accessibility test error: {e}")
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
    
    # No cleanup needed - using existing testuser@example.com account
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_backend_tests():
    """Run focused tests for AI Video Generation with Image URL Fix"""
    print("🚀 Testing AI Video Generation with Image URL Fix")
    print("=" * 70)
    print("Focus: Verify images stored as URLs instead of base64 to avoid MongoDB 16MB limit")
    print("=" * 70)
    
    tester = BackendTester()
    test_results = {}
    
    try:
        # Test 1: Login with testuser@example.com / password123
        print("\n" + "="*50)
        print("TEST 1: Create New Video Project")
        print("="*50)
        test_results['jwt_login'] = await tester.test_jwt_login()
        
        if not test_results['jwt_login']:
            print("❌ Cannot proceed without authentication")
            return test_results
        
        # Test 2: Create video project with specific prompt
        test_results['video_generation'] = await tester.test_video_generation()
        
        if not test_results['video_generation']:
            print("❌ Cannot proceed without video project")
            return test_results
        
        # Test 3: Monitor video generation progress
        print("\n" + "="*50)
        print("TEST 2: Monitor Video Generation Progress")
        print("="*50)
        test_results['project_status_polling'] = await tester.test_project_status_polling()
        
        # Test 4: Verify image accessibility
        print("\n" + "="*50)
        print("TEST 3: Verify Generated Content")
        print("="*50)
        test_results['image_accessibility'] = await tester.test_image_accessibility()
        
        # Additional verification
        print("\n" + "="*50)
        print("TEST 4: Verify Images Are Accessible")
        print("="*50)
        test_results['get_all_projects'] = await tester.test_get_all_projects()
        
    except Exception as e:
        print(f"\n❌ Critical test error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
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