#!/usr/bin/env python3
"""
FINAL Test - AI Video Generation with Image Generation (response_format removed)
Testing what format the Emergent API returns when response_format is not specified
"""

import asyncio
import httpx
import json
import time
from pymongo import MongoClient
from datetime import datetime

# Configuration
BACKEND_URL = "https://c-project-4.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database"

# Test credentials
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpassword123"
TEST_PROMPT = "A majestic mountain landscape at dawn"

class FinalImageTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=180.0)
        self.mongo_client = MongoClient(MONGO_URL)
        self.db = self.mongo_client[DB_NAME]
        self.access_token = None
        self.project_id = None
        
    async def ensure_test_user_exists(self):
        """Ensure test user exists in database"""
        print("🔧 Checking if test user exists...")
        
        user = self.db.users.find_one({'email': TEST_EMAIL})
        
        if not user:
            print(f"❌ Test user {TEST_EMAIL} not found in database")
            print("Creating test user...")
            
            # Import password hashing
            from passlib.context import CryptContext
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            
            hashed_password = pwd_context.hash(TEST_PASSWORD)
            
            user_doc = {
                'email': TEST_EMAIL,
                'name': 'Test User',
                'password': hashed_password,
                'subscription_plan': 'free',
                'videos_created': 0,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            self.db.users.insert_one(user_doc)
            print(f"✅ Created test user: {TEST_EMAIL}")
        else:
            print(f"✅ Test user exists: {TEST_EMAIL}")
    
    async def test_jwt_login(self):
        """Test JWT login with testuser@example.com"""
        print("\n" + "="*70)
        print("🔐 TEST 1: JWT Login")
        print("="*70)
        print(f"Email: {TEST_EMAIL}")
        print(f"Password: {TEST_PASSWORD}")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": TEST_EMAIL,
                    "password": TEST_PASSWORD
                }
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                user = data.get('user', {})
                
                print(f"✅ Login successful")
                print(f"   Access Token: {self.access_token[:50]}...")
                print(f"   User ID: {user.get('id')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Name: {user.get('name')}")
                print(f"   Subscription: {user.get('subscription_plan')}")
                return True
            else:
                print(f"❌ Login failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_create_video_project(self):
        """Test creating a video project"""
        print("\n" + "="*70)
        print("🎬 TEST 2: Create Video Project")
        print("="*70)
        print(f"Prompt: {TEST_PROMPT}")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        try:
            response = await self.client.post(
                f"{API_BASE}/video/generate",
                json={
                    "title": "Mountain Landscape Video",
                    "input_text": TEST_PROMPT
                },
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                project = response.json()
                self.project_id = project.get('id')
                
                print(f"✅ Video project created")
                print(f"   Project ID: {self.project_id}")
                print(f"   Title: {project.get('title')}")
                print(f"   Status: {project.get('status')}")
                return True
            else:
                print(f"❌ Failed to create project: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Create project error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_wait_for_completion(self):
        """Wait for video generation to complete and verify image format"""
        print("\n" + "="*70)
        print("⏳ TEST 3: Wait for Video Generation & Verify Images")
        print("="*70)
        print(f"Project ID: {self.project_id}")
        print("Polling every 5 seconds, timeout: 90 seconds")
        
        if not self.project_id or not self.access_token:
            print("❌ Missing project ID or access token")
            return False
        
        start_time = time.time()
        timeout = 90
        poll_interval = 5
        
        try:
            while time.time() - start_time < timeout:
                elapsed = int(time.time() - start_time)
                
                response = await self.client.get(
                    f"{API_BASE}/video/projects/{self.project_id}",
                    headers={"Authorization": f"Bearer {self.access_token}"}
                )
                
                if response.status_code != 200:
                    print(f"❌ Failed to get project status: {response.text}")
                    return False
                
                project = response.json()
                status = project.get('status')
                
                print(f"[{elapsed}s] Status: {status}")
                
                if status == 'completed':
                    print(f"\n✅ Video generation completed in {elapsed} seconds!")
                    return await self.verify_image_format(project)
                    
                elif status == 'failed':
                    error_msg = project.get('error_message', 'Unknown error')
                    print(f"\n❌ Video generation failed: {error_msg}")
                    return False
                
                # Wait before next poll
                await asyncio.sleep(poll_interval)
            
            print(f"\n❌ Timeout reached ({timeout}s) - video generation did not complete")
            
            # Get final status
            response = await self.client.get(
                f"{API_BASE}/video/projects/{self.project_id}",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            if response.status_code == 200:
                project = response.json()
                print(f"Final status: {project.get('status')}")
                print(f"Error message: {project.get('error_message', 'None')}")
            
            return False
            
        except Exception as e:
            print(f"❌ Polling error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    async def verify_image_format(self, project):
        """Verify the format of image_url fields"""
        print("\n" + "="*70)
        print("🔍 CRITICAL VERIFICATION: Image URL Format")
        print("="*70)
        
        scenes = project.get('scenes', [])
        
        if not scenes:
            print("❌ No scenes found in project")
            return False
        
        print(f"Total scenes: {len(scenes)}")
        
        # Check each scene
        all_valid = True
        base64_count = 0
        url_count = 0
        placeholder_count = 0
        null_count = 0
        
        for i, scene in enumerate(scenes, 1):
            scene_num = scene.get('scene_number', i)
            image_url = scene.get('image_url')
            
            print(f"\n--- Scene {scene_num} ---")
            print(f"Description: {scene.get('description', 'N/A')[:80]}...")
            print(f"Image Prompt: {scene.get('image_prompt', 'N/A')[:80]}...")
            
            if image_url is None:
                print(f"❌ Image URL: NULL")
                null_count += 1
                all_valid = False
            elif image_url.startswith('data:image/png;base64,'):
                print(f"✅ Image URL: Base64 data URL")
                base64_count += 1
                # Show first 200 characters
                print(f"   First 200 chars: {image_url[:200]}")
            elif image_url.startswith('http://') or image_url.startswith('https://'):
                if 'placeholder' in image_url.lower():
                    print(f"❌ Image URL: Placeholder URL")
                    print(f"   URL: {image_url}")
                    placeholder_count += 1
                    all_valid = False
                else:
                    print(f"✅ Image URL: HTTP URL")
                    print(f"   URL: {image_url[:100]}...")
                    url_count += 1
                    
                    # Try to verify it's a valid image
                    try:
                        img_response = await self.client.head(image_url, timeout=10.0)
                        content_type = img_response.headers.get('content-type', '')
                        if 'image' in content_type:
                            print(f"   ✅ Valid image (Content-Type: {content_type})")
                        else:
                            print(f"   ⚠️  Not an image (Content-Type: {content_type})")
                    except Exception as e:
                        print(f"   ⚠️  Could not verify URL: {e}")
            else:
                print(f"❌ Image URL: Unknown format")
                print(f"   Value: {image_url[:200]}")
                all_valid = False
        
        # Summary
        print("\n" + "="*70)
        print("📊 IMAGE FORMAT SUMMARY")
        print("="*70)
        print(f"Total scenes: {len(scenes)}")
        print(f"Base64 data URLs: {base64_count}")
        print(f"HTTP URLs: {url_count}")
        print(f"Placeholder URLs: {placeholder_count}")
        print(f"NULL values: {null_count}")
        
        if all_valid and (base64_count > 0 or url_count > 0):
            print("\n✅ SUCCESS: All images have valid URLs (base64 or HTTP)")
            
            # Show samples from at least 2 different images
            print("\n📸 Sample Image Data (first 200 chars from 2 different images):")
            sample_count = 0
            for i, scene in enumerate(scenes, 1):
                image_url = scene.get('image_url')
                if image_url and not ('placeholder' in image_url.lower()) and sample_count < 2:
                    sample_count += 1
                    print(f"\nScene {scene.get('scene_number', i)}:")
                    print(f"{image_url[:200]}")
            
            return True
        else:
            print("\n❌ FAILURE: Some images are missing, null, or placeholders")
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()
        self.mongo_client.close()

async def run_final_test():
    """Run the final image generation test"""
    print("🚀 FINAL TEST - AI Video Generation with Image Generation")
    print("Testing what format Emergent API returns without response_format parameter")
    print("="*70)
    
    tester = FinalImageTester()
    
    try:
        # Ensure test user exists
        await tester.ensure_test_user_exists()
        
        # Run tests
        test1 = await tester.test_jwt_login()
        if not test1:
            print("\n❌ Login failed, cannot continue")
            return False
        
        test2 = await tester.test_create_video_project()
        if not test2:
            print("\n❌ Project creation failed, cannot continue")
            return False
        
        test3 = await tester.test_wait_for_completion()
        
        # Final result
        print("\n" + "="*70)
        print("🏁 FINAL TEST RESULT")
        print("="*70)
        
        if test3:
            print("✅ ALL TESTS PASSED")
            print("Image generation is working correctly!")
            return True
        else:
            print("❌ TEST FAILED")
            print("Image generation has issues - check details above")
            return False
        
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        await tester.close()

if __name__ == "__main__":
    result = asyncio.run(run_final_test())
    exit(0 if result else 1)
