#!/usr/bin/env python3
"""
Test AI video generation with Emergent LLM Key
Tests the specific user request: Login, create video, monitor status
"""

import asyncio
import httpx
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

# Test credentials
TEST_EMAIL = "testuser@example.com"
TEST_PASSWORD = "Test123!"

# Test video data
VIDEO_DATA = {
    "title": "Emergent Test Video",
    "input_text": "Create a short 3-scene video about how artificial intelligence is revolutionizing healthcare with AI-powered diagnostics"
}

class EmergentLLMTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=180.0)
        self.access_token = None
        self.project_id = None
        
    async def test_login(self):
        """Test 1: Login with testuser@example.com"""
        print("=" * 70)
        print("TEST 1: Login with testuser@example.com")
        print("=" * 70)
        
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
                print(f"   Access Token: {self.access_token[:20]}...")
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
    
    async def test_create_video(self):
        """Test 2: Create video project"""
        print("\n" + "=" * 70)
        print("TEST 2: Create Video Project")
        print("=" * 70)
        print(f"Title: {VIDEO_DATA['title']}")
        print(f"Input: {VIDEO_DATA['input_text']}")
        
        if not self.access_token:
            print("❌ No access token - login first")
            return False
        
        try:
            response = await self.client.post(
                f"{API_BASE}/video/generate",
                json=VIDEO_DATA,
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"\nStatus Code: {response.status_code}")
            
            if response.status_code == 200:
                project = response.json()
                self.project_id = project.get('id')
                
                print(f"✅ VIDEO PROJECT CREATED")
                print(f"   Project ID: {self.project_id}")
                print(f"   Title: {project.get('title')}")
                print(f"   Status: {project.get('status')}")
                print(f"   User ID: {project.get('user_id')}")
                print(f"   Created At: {project.get('created_at')}")
                
                # Verify status is "pending"
                if project.get('status') == 'pending':
                    print(f"   ✅ Status is 'pending' as expected")
                else:
                    print(f"   ⚠️  Status is '{project.get('status')}' (expected 'pending')")
                
                return True
            else:
                print(f"❌ VIDEO CREATION FAILED")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ VIDEO CREATION ERROR: {e}")
            return False
    
    async def test_monitor_project(self):
        """Test 3: Monitor project for 30 seconds"""
        print("\n" + "=" * 70)
        print("TEST 3: Monitor Project Status (30 seconds)")
        print("=" * 70)
        
        if not self.project_id:
            print("❌ No project ID - create video first")
            return False
        
        print(f"Project ID: {self.project_id}")
        print(f"Checking every 5 seconds for 30 seconds...")
        print()
        
        start_time = time.time()
        timeout = 30
        check_interval = 5
        
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
                
                # Track status progression
                if not status_progression or status_progression[-1] != status:
                    status_progression.append(status)
                
                print(f"[{elapsed}s] Status: {status}")
                
                # Show additional details based on status
                if status == 'generating_script':
                    print(f"       → GPT-4o generating script...")
                elif status == 'generating_images':
                    scenes = project.get('scenes', [])
                    print(f"       → gpt-image-1 generating images for {len(scenes)} scenes...")
                elif status == 'completed':
                    print(f"\n✅ VIDEO GENERATION COMPLETED!")
                    self._print_completion_details(project)
                    return True
                elif status == 'failed':
                    error_msg = project.get('error_message', 'Unknown error')
                    print(f"\n❌ VIDEO GENERATION FAILED")
                    print(f"   Error: {error_msg}")
                    return False
                
                # Wait before next check
                await asyncio.sleep(check_interval)
            
            # Timeout reached
            print(f"\n⏱️  MONITORING TIMEOUT (30 seconds)")
            print(f"   Status progression: {' → '.join(status_progression)}")
            print(f"   Final status: {status_progression[-1] if status_progression else 'unknown'}")
            
            # Get final project state
            response = await self.client.get(
                f"{API_BASE}/video/projects/{self.project_id}",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            if response.status_code == 200:
                project = response.json()
                print(f"\n   Final Project State:")
                print(f"   - Status: {project.get('status')}")
                print(f"   - Scenes: {len(project.get('scenes', []))}")
                print(f"   - Duration: {project.get('duration', 0)}s")
                
                if project.get('status') in ['generating_script', 'generating_images', 'processing']:
                    print(f"\n   ℹ️  Video is still processing (may take longer than 30s)")
                    print(f"   ℹ️  This is normal for AI video generation")
            
            return False
                
        except Exception as e:
            print(f"❌ MONITORING ERROR: {e}")
            return False
    
    def _print_completion_details(self, project):
        """Print detailed completion information"""
        scenes = project.get('scenes', [])
        duration = project.get('duration', 0)
        thumbnail = project.get('thumbnail_url')
        
        print(f"   Total Scenes: {len(scenes)}")
        print(f"   Total Duration: {duration}s")
        print(f"   Thumbnail: {'✅ Generated' if thumbnail else '❌ Missing'}")
        
        # Verify script generation (GPT-4o)
        print(f"\n   📝 Script Generation (GPT-4o):")
        if scenes:
            has_descriptions = all(s.get('description') for s in scenes)
            has_narrations = all(s.get('narration') for s in scenes)
            print(f"      - Descriptions: {'✅ All scenes' if has_descriptions else '❌ Missing'}")
            print(f"      - Narrations: {'✅ All scenes' if has_narrations else '❌ Missing'}")
        else:
            print(f"      ❌ No scenes generated")
        
        # Verify image generation (gpt-image-1)
        print(f"\n   🖼️  Image Generation (gpt-image-1):")
        if scenes:
            scenes_with_images = sum(1 for s in scenes if s.get('image_url'))
            print(f"      - Images: {scenes_with_images}/{len(scenes)} scenes")
            
            for i, scene in enumerate(scenes, 1):
                image_url = scene.get('image_url', '')
                has_image = bool(image_url)
                is_base64 = image_url.startswith('data:image') if image_url else False
                print(f"      - Scene {i}: {'✅ Base64 image' if is_base64 else '❌ No image'}")
        else:
            print(f"      ❌ No scenes to generate images for")
        
        # Show sample scene
        if scenes:
            print(f"\n   📄 Sample Scene (Scene 1):")
            scene = scenes[0]
            print(f"      - Scene Number: {scene.get('scene_number')}")
            print(f"      - Description: {scene.get('description', '')[:80]}...")
            print(f"      - Narration: {scene.get('narration', '')[:80]}...")
            print(f"      - Image Prompt: {scene.get('image_prompt', '')[:80]}...")
            print(f"      - Duration: {scene.get('duration', 0)}s")
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def main():
    """Run the Emergent LLM test"""
    print("\n🚀 EMERGENT LLM KEY TEST - AI VIDEO GENERATION")
    print("Testing: GPT-4o (script) + gpt-image-1 (images)")
    print("=" * 70)
    
    tester = EmergentLLMTester()
    results = {}
    
    try:
        # Test 1: Login
        results['login'] = await tester.test_login()
        
        if not results['login']:
            print("\n❌ Cannot proceed without successful login")
            return
        
        # Test 2: Create video
        results['create_video'] = await tester.test_create_video()
        
        if not results['create_video']:
            print("\n❌ Cannot proceed without successful video creation")
            return
        
        # Test 3: Monitor project
        results['monitor_project'] = await tester.test_monitor_project()
        
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
    
    finally:
        await tester.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():<30} {status}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Emergent LLM integration working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check details above.")

if __name__ == "__main__":
    asyncio.run(main())
