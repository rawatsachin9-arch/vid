#!/usr/bin/env python3
"""
Authentication System Testing
Tests JWT-based register, login, and get current user endpoints
"""

import asyncio
import httpx
import json
import time
import random
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8001"
API_BASE = f"{BACKEND_URL}/api"

class AuthTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.access_token = None
        self.user_email = None
        self.user_password = "TestPassword123!"
        self.user_name = "Test User"
        
    async def test_register(self):
        """Test POST /api/auth/register endpoint"""
        print("\n🔐 Testing User Registration - POST /api/auth/register")
        
        # Generate unique email
        random_suffix = random.randint(10000, 99999)
        self.user_email = f"logintest{random_suffix}@example.com"
        
        register_data = {
            "email": self.user_email,
            "password": self.user_password,
            "name": self.user_name
        }
        
        print(f"   Email: {self.user_email}")
        print(f"   Name: {self.user_name}")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/register",
                json=register_data
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                if 'access_token' not in data:
                    print(f"❌ Missing access_token in response")
                    return False
                
                if 'user' not in data:
                    print(f"❌ Missing user object in response")
                    return False
                
                self.access_token = data['access_token']
                user = data['user']
                
                print(f"✅ Registration successful")
                print(f"   Access Token: {self.access_token[:20]}...")
                print(f"   User ID: {user.get('id')}")
                print(f"   User Email: {user.get('email')}")
                print(f"   User Name: {user.get('name')}")
                print(f"   Subscription Plan: {user.get('subscription_plan')}")
                
                # Verify user data matches
                if user.get('email') != self.user_email:
                    print(f"❌ Email mismatch: expected {self.user_email}, got {user.get('email')}")
                    return False
                
                if user.get('name') != self.user_name:
                    print(f"❌ Name mismatch: expected {self.user_name}, got {user.get('name')}")
                    return False
                
                return True
            else:
                print(f"❌ Registration failed")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Registration test error: {e}")
            return False
    
    async def test_login(self):
        """Test POST /api/auth/login endpoint"""
        print("\n🔐 Testing User Login - POST /api/auth/login")
        
        if not self.user_email:
            print("❌ No user email available (registration must run first)")
            return False
        
        login_data = {
            "email": self.user_email,
            "password": self.user_password
        }
        
        print(f"   Email: {self.user_email}")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json=login_data
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify response structure
                if 'access_token' not in data:
                    print(f"❌ Missing access_token in response")
                    return False
                
                if 'user' not in data:
                    print(f"❌ Missing user object in response")
                    return False
                
                # Update access token from login
                self.access_token = data['access_token']
                user = data['user']
                
                print(f"✅ Login successful")
                print(f"   Access Token: {self.access_token[:20]}...")
                print(f"   User ID: {user.get('id')}")
                print(f"   User Email: {user.get('email')}")
                print(f"   User Name: {user.get('name')}")
                print(f"   Subscription Plan: {user.get('subscription_plan')}")
                
                # Verify user data matches
                if user.get('email') != self.user_email:
                    print(f"❌ Email mismatch: expected {self.user_email}, got {user.get('email')}")
                    return False
                
                if user.get('name') != self.user_name:
                    print(f"❌ Name mismatch: expected {self.user_name}, got {user.get('name')}")
                    return False
                
                return True
            else:
                print(f"❌ Login failed")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login test error: {e}")
            return False
    
    async def test_get_current_user(self):
        """Test GET /api/auth/me endpoint"""
        print("\n🔐 Testing Get Current User - GET /api/auth/me")
        
        if not self.access_token:
            print("❌ No access token available (login must run first)")
            return False
        
        print(f"   Using Bearer Token: {self.access_token[:20]}...")
        
        try:
            response = await self.client.get(
                f"{API_BASE}/auth/me",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                user = response.json()
                
                print(f"✅ Get current user successful")
                print(f"   User ID: {user.get('id')}")
                print(f"   Email: {user.get('email')}")
                print(f"   Name: {user.get('name')}")
                print(f"   Subscription Plan: {user.get('subscription_plan')}")
                print(f"   Videos Created: {user.get('videos_created')}")
                print(f"   Created At: {user.get('created_at')}")
                
                # Verify user data matches
                if user.get('email') != self.user_email:
                    print(f"❌ Email mismatch: expected {self.user_email}, got {user.get('email')}")
                    return False
                
                if user.get('name') != self.user_name:
                    print(f"❌ Name mismatch: expected {self.user_name}, got {user.get('name')}")
                    return False
                
                return True
            else:
                print(f"❌ Get current user failed")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Get current user test error: {e}")
            return False
    
    async def test_invalid_login(self):
        """Test login with invalid credentials"""
        print("\n🔐 Testing Invalid Login - POST /api/auth/login")
        
        if not self.user_email:
            print("❌ No user email available")
            return False
        
        login_data = {
            "email": self.user_email,
            "password": "WrongPassword123!"
        }
        
        print(f"   Email: {self.user_email}")
        print(f"   Password: WrongPassword123! (intentionally wrong)")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json=login_data
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 401:
                print(f"✅ Invalid login correctly rejected with 401")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Expected 401 status code, got {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Invalid login test error: {e}")
            return False
    
    async def test_unauthorized_access(self):
        """Test accessing /api/auth/me without token"""
        print("\n🔐 Testing Unauthorized Access - GET /api/auth/me (no token)")
        
        try:
            response = await self.client.get(f"{API_BASE}/auth/me")
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 401:
                print(f"✅ Unauthorized access correctly rejected with 401")
                print(f"   Response: {response.json()}")
                return True
            else:
                print(f"❌ Expected 401 status code, got {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Unauthorized access test error: {e}")
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_auth_tests():
    """Run all authentication tests"""
    print("🚀 Starting Authentication System Tests")
    print("=" * 70)
    
    tester = AuthTester()
    test_results = {}
    
    try:
        # Core authentication flow
        test_results['register'] = await tester.test_register()
        test_results['login'] = await tester.test_login()
        test_results['get_current_user'] = await tester.test_get_current_user()
        
        # Security tests
        test_results['invalid_login'] = await tester.test_invalid_login()
        test_results['unauthorized_access'] = await tester.test_unauthorized_access()
        
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
        print(f"{test_name.replace('_', ' ').title():<35} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All authentication tests passed! Login system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the detailed output above.")
    
    return test_results

if __name__ == "__main__":
    asyncio.run(run_auth_tests())
