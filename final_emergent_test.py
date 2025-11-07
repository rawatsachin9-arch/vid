#!/usr/bin/env python3
"""
FINAL TEST: AI Video Generation with Emergent LLM Key
Tests GPT-4o text generation and gpt-image-1 image generation
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
    "title": "Final Test",
    "input_text": "Create a 3-scene video about AI revolutionizing healthcare"
}

class EmergentVideoTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=180.0)  # 180-second timeout
        self.access_token = None
        self.project_id = None
        
    async def test_login(self):
        """Test 1: Login to get access token"""
        print("\n" + "="*70)
        print("TEST 1: Login with JWT Authentication")
        print("="*70)
        print(f"📧 Email: {TEST_EMAIL}")
        print(f"🔒 Password: {TEST_PASSWORD}")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                user = data.get('user', {})
                
                print(f"✅ LOGIN SUCCESSFUL")
                print(f"   Access Token: {self.access_token[:50]}...")
                print(f"   User ID: {user.get('id')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Name: {user.get('name')}")
                print(f"   Subscription: {user.get('subscription_plan')}")
                return True
            else:
                print(f"❌ LOGIN FAILED")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ LOGIN ERROR: {e}")
            return False
    
    async def test_create_video_project(self):
        """Test 2: Create video project"""
        print("\n" + "="*70)
        print("TEST 2: Create Video Project")
        print("="*70)
        print(f"📝 Title: {TEST_VIDEO_DATA['title']}")
        print(f"📄 Input: {TEST_VIDEO_DATA['input_text']}")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        try:
            response = await self.client.post(
                f"{API_BASE}/video/generate",
                json=TEST_VIDEO_DATA,
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                project = response.json()
                self.project_id = project.get('id')
                
                print(f"✅ PROJECT CREATED")
                print(f"   Project ID: {self.project_id}")
                print(f"   Status: {project.get('status')}")
                print(f"   Title: {project.get('title')}")
                print(f"   User ID: {project.get('user_id')}")
                
                if project.get('status') == 'pending':
                    print(f"   ✅ Status is 'pending' as expected")
                    return True
                else:
                    print(f"   ⚠️  Status is '{project.get('status')}' instead of 'pending'")
                    return False
            else:
                print(f"❌ PROJECT CREATION FAILED")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ PROJECT CREATION ERROR: {e}")
            return False
    
    async def test_monitor_video_generation(self):
        """Test 3: Monitor video generation for 60 seconds"""
        print("\n" + "="*70)
        print("TEST 3: Monitor Video Generation (60 seconds)")
        print("="*70)
        print(f"🎬 Project ID: {self.project_id}")
        print(f"⏱️  Polling every 10 seconds...")
        print(f"⏱️  Timeout: 60 seconds")
        
        if not self.project_id or not self.access_token:
            print("❌ No project ID or access token available")
            return False
        
        start_time = time.time()
        timeout = 60  # 60 seconds as requested
        poll_interval = 10  # Poll every 10 seconds
        
        status_progression = []
        
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
                error_message = project.get('error_message')
                
                # Track status progression
                if not status_progression or status_progression[-1] != status:
                    status_progression.append(status)
                
                print(f"\n[{elapsed}s] Status: {status}")
                
                # Check for completion
                if status == 'completed':
                    print(f"\n✅ VIDEO GENERATION COMPLETED!")
                    print(f"   Total time: {elapsed} seconds")
                    print(f"   Status progression: {' → '.join(status_progression)}")
                    
                    # Verify scenes
                    scenes = project.get('scenes', [])
                    print(f"\n📊 VERIFICATION:")
                    print(f"   Total scenes: {len(scenes)}")
                    print(f"   Duration: {project.get('duration', 0)} seconds")
                    print(f"   Thumbnail URL: {'✅ Present' if project.get('thumbnail_url') else '❌ Missing'}")
                    
                    # Check each scene
                    scenes_with_images = 0
                    scenes_with_base64 = 0
                    
                    for i, scene in enumerate(scenes, 1):
                        has_image = bool(scene.get('image_url'))
                        is_base64 = scene.get('image_url', '').startswith('data:image')
                        
                        if has_image:
                            scenes_with_images += 1
                        if is_base64:
                            scenes_with_base64 += 1
                        
                        print(f"\n   Scene {i}:")
                        print(f"     - Scene number: {scene.get('scene_number')}")
                        print(f"     - Description: {scene.get('description', '')[:60]}...")
                        print(f"     - Narration: {scene.get('narration', '')[:60]}...")
                        print(f"     - Image prompt: {scene.get('image_prompt', '')[:60]}...")
                        print(f"     - Image URL: {'✅ Base64 data' if is_base64 else '❌ Missing/Invalid'}")
                        print(f"     - Duration: {scene.get('duration', 0)}s")
                    
                    print(f"\n📈 SUMMARY:")
                    print(f"   Scenes with images: {scenes_with_images}/{len(scenes)}")
                    print(f"   Scenes with base64 data: {scenes_with_base64}/{len(scenes)}")
                    
                    # Success criteria
                    success = True
                    print(f"\n🎯 SUCCESS CRITERIA:")
                    
                    if len(scenes) > 0:
                        print(f"   ✅ Script generated successfully with GPT-4o")
                    else:
                        print(f"   ❌ No scenes generated")
                        success = False
                    
                    if scenes_with_base64 == len(scenes) and len(scenes) > 0:
                        print(f"   ✅ Images generated successfully with gpt-image-1")
                        print(f"   ✅ All scenes have image_url (base64 data URLs)")
                    else:
                        print(f"   ❌ Not all scenes have base64 images ({scenes_with_base64}/{len(scenes)})")
                        success = False
                    
                    if status == 'completed':
                        print(f"   ✅ Status reached 'completed'")
                    else:
                        print(f"   ❌ Status is '{status}' not 'completed'")
                        success = False
                    
                    return success
                
                # Check for failure
                elif status == 'failed':
                    print(f"\n❌ VIDEO GENERATION FAILED")
                    print(f"   Error message: {error_message}")
                    print(f"   Status progression: {' → '.join(status_progression)}")
                    return False
                
                # Show progress for other statuses
                elif status in ['processing', 'generating_script', 'generating_images']:
                    print(f"   ⏳ In progress...")
                
                # Wait before next poll
                await asyncio.sleep(poll_interval)
            
            # Timeout reached
            print(f"\n⏱️  TIMEOUT REACHED (60 seconds)")
            print(f"   Final status: {status}")
            print(f"   Status progression: {' → '.join(status_progression)}")
            print(f"   ⚠️  Video generation did not complete within 60 seconds")
            print(f"   Note: Image generation can take up to 1 minute per scene")
            
            # Get final project state
            response = await self.client.get(
                f"{API_BASE}/video/projects/{self.project_id}",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            if response.status_code == 200:
                project = response.json()
                scenes = project.get('scenes', [])
                print(f"\n   Current progress:")
                print(f"     - Scenes: {len(scenes)}")
                print(f"     - Status: {project.get('status')}")
                if project.get('error_message'):
                    print(f"     - Error: {project.get('error_message')}")
            
            return False
            
        except Exception as e:
            print(f"❌ MONITORING ERROR: {e}")
            import traceback
            print(traceback.format_exc())
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_final_test():
    """Run the final Emergent LLM Key test"""
    print("\n" + "="*70)
    print("🚀 FINAL TEST: AI Video Generation with Emergent LLM Key")
    print("="*70)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔑 Using: Emergent LLM Key for GPT-4o + gpt-image-1")
    print(f"⏱️  Timeout: 180 seconds for API calls, 60 seconds for monitoring")
    
    tester = EmergentVideoTester()
    results = {}
    
    try:
        # Test 1: Login
        results['login'] = await tester.test_login()
        
        if not results['login']:
            print("\n❌ Cannot proceed without successful login")
            return results
        
        # Test 2: Create video project
        results['create_project'] = await tester.test_create_video_project()
        
        if not results['create_project']:
            print("\n❌ Cannot proceed without successful project creation")
            return results
        
        # Test 3: Monitor video generation
        results['video_generation'] = await tester.test_monitor_video_generation()
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        print(traceback.format_exc())
    
    finally:
        await tester.close()
    
    # Final summary
    print("\n" + "="*70)
    print("📊 FINAL TEST RESULTS")
    print("="*70)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():<30} {status}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Emergent LLM Key integration working correctly.")
    else:
        print("\n⚠️  SOME TESTS FAILED. Check detailed output above.")
    
    print("="*70)
    
    return results

if __name__ == "__main__":
    asyncio.run(run_final_test())
