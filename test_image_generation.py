#!/usr/bin/env python3
"""
Test AI Video Generation with Image Generation
Specifically tests that images are generated as base64 data URLs, not placeholders
"""

import asyncio
import httpx
import json
import time
from datetime import datetime

# Configuration - Use the actual backend URL from frontend/.env
BACKEND_URL = "https://c-project-4.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials as specified by user
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "testpassword123"

# Test video prompt as specified by user
TEST_PROMPT = "A peaceful garden with colorful flowers blooming"

class ImageGenerationTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=180.0)
        self.access_token = None
        self.project_id = None
        
    async def test_jwt_login(self):
        """Test JWT login with testuser@example.com"""
        print("=" * 80)
        print("🔐 TEST 1: JWT Login")
        print("=" * 80)
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
            
            print(f"\nStatus Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                user = data.get('user', {})
                
                print("✅ LOGIN SUCCESSFUL")
                print(f"   Access Token: {self.access_token[:50]}...")
                print(f"   User ID: {user.get('id')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Name: {user.get('name')}")
                print(f"   Subscription Plan: {user.get('subscription_plan')}")
                return True
            else:
                print(f"❌ LOGIN FAILED")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ LOGIN ERROR: {e}")
            return False
    
    async def test_create_video_project(self):
        """Create a new video project"""
        print("\n" + "=" * 80)
        print("🎬 TEST 2: Create Video Project")
        print("=" * 80)
        print(f"Prompt: {TEST_PROMPT}")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        try:
            response = await self.client.post(
                f"{API_BASE}/video/generate",
                json={
                    "title": "Sunset Video Test",
                    "input_text": TEST_PROMPT
                },
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"\nStatus Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.project_id = data.get('id')
                
                print("✅ PROJECT CREATED SUCCESSFULLY")
                print(f"   Project ID: {self.project_id}")
                print(f"   Title: {data.get('title')}")
                print(f"   Status: {data.get('status')}")
                print(f"   User ID: {data.get('user_id')}")
                return True
            else:
                print(f"❌ PROJECT CREATION FAILED")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ PROJECT CREATION ERROR: {e}")
            return False
    
    async def test_video_generation_with_images(self):
        """Poll project status and verify image generation"""
        print("\n" + "=" * 80)
        print("🖼️  TEST 3: Video Generation with Image Verification")
        print("=" * 80)
        print(f"Project ID: {self.project_id}")
        print("Polling every 5 seconds for up to 60 seconds...")
        
        if not self.project_id or not self.access_token:
            print("❌ Missing project ID or access token")
            return False
        
        start_time = time.time()
        timeout = 60  # 60 seconds as specified
        poll_interval = 5  # 5 seconds as specified
        
        try:
            while time.time() - start_time < timeout:
                response = await self.client.get(
                    f"{API_BASE}/video/projects/{self.project_id}",
                    headers={"Authorization": f"Bearer {self.access_token}"}
                )
                
                if response.status_code != 200:
                    print(f"❌ Failed to get project status: {response.text}")
                    return False
                
                project = response.json()
                status = project.get('status')
                elapsed = int(time.time() - start_time)
                
                print(f"\n[{elapsed}s] Status: {status}")
                
                if status == 'completed':
                    return await self._verify_completed_project(project)
                    
                elif status == 'failed':
                    error_msg = project.get('error_message', 'Unknown error')
                    print(f"\n❌ VIDEO GENERATION FAILED")
                    print(f"   Error: {error_msg}")
                    return False
                
                # Wait before next poll
                await asyncio.sleep(poll_interval)
            
            print(f"\n❌ TIMEOUT REACHED ({timeout}s)")
            print("   Video generation did not complete in time")
            return False
            
        except Exception as e:
            print(f"\n❌ POLLING ERROR: {e}")
            return False
    
    async def _verify_completed_project(self, project):
        """Verify the completed project has valid images"""
        print("\n✅ VIDEO GENERATION COMPLETED")
        
        scenes = project.get('scenes', [])
        duration = project.get('duration', 0)
        thumbnail_url = project.get('thumbnail_url')
        
        print(f"\n📊 PROJECT DETAILS:")
        print(f"   Status: {project.get('status')}")
        print(f"   Total Scenes: {len(scenes)}")
        print(f"   Duration: {duration} seconds")
        print(f"   Thumbnail URL: {'✅ Present' if thumbnail_url else '❌ Missing'}")
        
        # Verify we have 5 scenes
        if len(scenes) != 5:
            print(f"\n❌ SCENE COUNT MISMATCH")
            print(f"   Expected: 5 scenes")
            print(f"   Actual: {len(scenes)} scenes")
            return False
        
        print(f"\n🔍 VERIFYING SCENE STRUCTURE AND IMAGES:")
        print("=" * 80)
        
        all_valid = True
        scenes_with_valid_images = 0
        scenes_with_placeholders = 0
        scenes_with_missing_images = 0
        
        for i, scene in enumerate(scenes, 1):
            scene_number = scene.get('scene_number')
            description = scene.get('description', '')
            narration = scene.get('narration', '')
            image_prompt = scene.get('image_prompt', '')
            scene_duration = scene.get('duration', 0)
            image_url = scene.get('image_url', '')
            
            print(f"\n📹 SCENE {i}:")
            print(f"   Scene Number: {scene_number}")
            print(f"   Description: {description[:80]}{'...' if len(description) > 80 else ''}")
            print(f"   Narration: {narration[:80]}{'...' if len(narration) > 80 else ''}")
            print(f"   Image Prompt: {image_prompt[:80]}{'...' if len(image_prompt) > 80 else ''}")
            print(f"   Duration: {scene_duration} seconds")
            
            # CRITICAL: Verify image_url
            if not image_url:
                print(f"   ❌ Image URL: MISSING (null or empty)")
                scenes_with_missing_images += 1
                all_valid = False
            elif 'placeholder' in image_url.lower():
                print(f"   ❌ Image URL: PLACEHOLDER DETECTED")
                print(f"      Value: {image_url}")
                scenes_with_placeholders += 1
                all_valid = False
            elif image_url.startswith('data:image/png;base64,'):
                # Valid base64 image data
                base64_length = len(image_url) - len('data:image/png;base64,')
                print(f"   ✅ Image URL: VALID BASE64 DATA")
                print(f"      Format: data:image/png;base64,...")
                print(f"      Base64 Length: {base64_length} characters")
                print(f"      First 100 chars: {image_url[:100]}...")
                scenes_with_valid_images += 1
            elif image_url.startswith('data:image/'):
                # Valid data URL but different format
                print(f"   ⚠️  Image URL: DATA URL (different format)")
                print(f"      Value: {image_url[:100]}...")
                scenes_with_valid_images += 1
            elif image_url.startswith('http'):
                # HTTP URL (might be placeholder)
                print(f"   ⚠️  Image URL: HTTP URL (not base64)")
                print(f"      Value: {image_url}")
                if 'placeholder' in image_url.lower():
                    scenes_with_placeholders += 1
                    all_valid = False
            else:
                print(f"   ❌ Image URL: UNKNOWN FORMAT")
                print(f"      Value: {image_url[:100]}...")
                all_valid = False
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 IMAGE GENERATION SUMMARY:")
        print("=" * 80)
        print(f"   Total Scenes: {len(scenes)}")
        print(f"   ✅ Valid Base64 Images: {scenes_with_valid_images}")
        print(f"   ❌ Placeholder Images: {scenes_with_placeholders}")
        print(f"   ❌ Missing Images: {scenes_with_missing_images}")
        
        if all_valid and scenes_with_valid_images == 5:
            print("\n🎉 SUCCESS: All scenes have valid base64 image data!")
            return True
        else:
            print("\n❌ FAILURE: Image generation is not working correctly")
            print("   Images are showing as placeholders or missing")
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_image_generation_test():
    """Run the complete image generation test"""
    print("\n" + "=" * 80)
    print("🚀 AI VIDEO GENERATION WITH IMAGE GENERATION TEST")
    print("=" * 80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test User: {TEST_EMAIL}")
    print(f"Test Prompt: {TEST_PROMPT}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)
    
    tester = ImageGenerationTester()
    
    try:
        # Test 1: JWT Login
        login_success = await tester.test_jwt_login()
        if not login_success:
            print("\n❌ CRITICAL: Login failed, cannot proceed with tests")
            return False
        
        # Test 2: Create Video Project
        create_success = await tester.test_create_video_project()
        if not create_success:
            print("\n❌ CRITICAL: Project creation failed, cannot proceed with tests")
            return False
        
        # Test 3: Verify Video Generation with Images
        generation_success = await tester.test_video_generation_with_images()
        
        # Final Result
        print("\n" + "=" * 80)
        print("🏁 FINAL TEST RESULT")
        print("=" * 80)
        
        if generation_success:
            print("✅ ALL TESTS PASSED")
            print("   - JWT authentication working")
            print("   - Video project creation working")
            print("   - GPT-4o script generation working")
            print("   - gpt-image-1 image generation working")
            print("   - Base64 image data correctly stored")
            return True
        else:
            print("❌ TESTS FAILED")
            print("   - Image generation is not working correctly")
            print("   - Images are showing as placeholders or missing")
            return False
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await tester.close()

if __name__ == "__main__":
    result = asyncio.run(run_image_generation_test())
    exit(0 if result else 1)
