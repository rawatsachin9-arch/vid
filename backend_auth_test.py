#!/usr/bin/env python3
"""
Backend Authentication System Testing
Focus: Password Reset Flow, Google OAuth Session Endpoint, Basic Authentication
"""

import asyncio
import httpx
import json
import time
import os
from datetime import datetime, timezone, timedelta

# Configuration - Use external URL from frontend/.env
BACKEND_URL = "https://core.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

class AuthTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_email = "testuser@example.com"
        self.original_password = "password123"
        self.new_password = "newpassword123"
        self.reset_token = None
        self.access_token = None
        
    async def test_basic_auth_register(self):
        """Test POST /api/auth/register"""
        print("🔐 Testing Basic Authentication - Register")
        
        # Use a unique email for registration test
        unique_email = f"regtest{int(time.time())}@example.com"
        register_data = {
            "email": unique_email,
            "password": "testpass123",
            "name": "Test User"
        }
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/register",
                json=register_data
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Registration successful")
                print(f"   Access Token: {result.get('access_token', '')[:20]}...")
                print(f"   User ID: {result.get('user', {}).get('id')}")
                print(f"   Email: {result.get('user', {}).get('email')}")
                return True
            else:
                print(f"❌ Registration failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False
    
    async def test_basic_auth_login(self):
        """Test POST /api/auth/login with original password"""
        print("\n🔐 Testing Basic Authentication - Login")
        
        login_data = {
            "email": self.test_email,
            "password": self.original_password
        }
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json=login_data
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.access_token = result.get('access_token')
                print(f"✅ Login successful")
                print(f"   Access Token: {self.access_token[:20]}...")
                print(f"   User ID: {result.get('user', {}).get('id')}")
                print(f"   Email: {result.get('user', {}).get('email')}")
                return True
            else:
                print(f"❌ Login failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login error: {e}")
            return False
    
    async def test_basic_auth_me(self):
        """Test GET /api/auth/me with Bearer token"""
        print("\n🔐 Testing Basic Authentication - Get Current User")
        
        if not self.access_token:
            print("❌ No access token available")
            return False
        
        try:
            response = await self.client.get(
                f"{API_BASE}/auth/me",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Get current user successful")
                print(f"   User ID: {result.get('id')}")
                print(f"   Email: {result.get('email')}")
                print(f"   Name: {result.get('name')}")
                print(f"   Subscription: {result.get('subscription_plan')}")
                return True
            else:
                print(f"❌ Get current user failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Get current user error: {e}")
            return False
    
    async def test_forgot_password(self):
        """Test POST /api/auth/forgot-password"""
        print("\n🔑 Testing Password Reset - Forgot Password")
        
        forgot_data = {
            "email": self.test_email
        }
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/forgot-password",
                json=forgot_data
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                self.reset_token = result.get('reset_token')
                print(f"✅ Forgot password successful")
                print(f"   Success: {result.get('success')}")
                print(f"   Message: {result.get('message')}")
                print(f"   Reset Token: {self.reset_token[:20] if self.reset_token else 'None'}...")
                
                # The endpoint returns success even if email doesn't exist for security
                # But it should return reset_token for existing users (in test mode)
                if result.get('success'):
                    return True
                else:
                    print("❌ Forgot password request failed")
                    return False
            else:
                print(f"❌ Forgot password failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Forgot password error: {e}")
            return False
    
    async def test_reset_password(self):
        """Test POST /api/auth/reset-password"""
        print("\n🔑 Testing Password Reset - Reset Password")
        
        if not self.reset_token:
            print("❌ No reset token available")
            return False
        
        reset_data = {
            "token": self.reset_token,
            "new_password": self.new_password
        }
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/reset-password",
                json=reset_data
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Password reset successful")
                print(f"   Success: {result.get('success')}")
                print(f"   Message: {result.get('message')}")
                return True
            else:
                print(f"❌ Password reset failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Password reset error: {e}")
            return False
    
    async def test_login_with_new_password(self):
        """Test POST /api/auth/login with new password after reset"""
        print("\n🔑 Testing Password Reset - Login with New Password")
        
        login_data = {
            "email": self.test_email,
            "password": self.new_password
        }
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json=login_data
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Login with new password successful")
                print(f"   Access Token: {result.get('access_token', '')[:20]}...")
                print(f"   User ID: {result.get('user', {}).get('id')}")
                print(f"   Email: {result.get('user', {}).get('email')}")
                return True
            else:
                print(f"❌ Login with new password failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login with new password error: {e}")
            return False
    
    async def test_google_oauth_missing_session(self):
        """Test POST /api/auth/google/session with missing session ID"""
        print("\n🔗 Testing Google OAuth - Missing Session ID")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/google/session",
                json={}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code in [400, 500]:
                result = response.json()
                error_detail = result.get('detail', '')
                if 'Session ID required' in error_detail:
                    print(f"✅ Correctly rejected missing session ID")
                    print(f"   Error: {error_detail}")
                    return True
                else:
                    print(f"❌ Unexpected error message: {error_detail}")
                    return False
            else:
                print(f"❌ Expected 400/500 error for missing session ID, got: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Google OAuth missing session test error: {e}")
            return False
    
    async def test_google_oauth_invalid_session(self):
        """Test POST /api/auth/google/session with invalid session ID"""
        print("\n🔗 Testing Google OAuth - Invalid Session ID")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/google/session",
                json={},
                headers={"X-Session-ID": "invalid_session_id_12345"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 401:
                result = response.json()
                print(f"✅ Correctly rejected invalid session ID")
                print(f"   Error: {result.get('detail')}")
                return True
            else:
                print(f"❌ Expected 401 error for invalid session ID, got: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Google OAuth invalid session test error: {e}")
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_auth_tests():
    """Run comprehensive authentication system tests"""
    print("🚀 Testing Backend Authentication System")
    print("=" * 70)
    print("Focus: Password Reset Flow, Google OAuth Session, Basic Authentication")
    print("=" * 70)
    
    tester = AuthTester()
    test_results = {}
    
    try:
        # Test 1: Basic Authentication Tests
        print("\n" + "="*50)
        print("TEST 1: Basic Authentication")
        print("="*50)
        
        test_results['register'] = await tester.test_basic_auth_register()
        test_results['login'] = await tester.test_basic_auth_login()
        test_results['get_me'] = await tester.test_basic_auth_me()
        
        # Test 2: Password Reset Flow
        print("\n" + "="*50)
        print("TEST 2: Password Reset Flow")
        print("="*50)
        
        test_results['forgot_password'] = await tester.test_forgot_password()
        
        if test_results['forgot_password']:
            test_results['reset_password'] = await tester.test_reset_password()
            
            if test_results['reset_password']:
                test_results['login_new_password'] = await tester.test_login_with_new_password()
            else:
                test_results['login_new_password'] = False
        else:
            test_results['reset_password'] = False
            test_results['login_new_password'] = False
        
        # Test 3: Google OAuth Session Endpoint
        print("\n" + "="*50)
        print("TEST 3: Google OAuth Session Endpoint")
        print("="*50)
        
        test_results['google_oauth_missing'] = await tester.test_google_oauth_missing_session()
        test_results['google_oauth_invalid'] = await tester.test_google_oauth_invalid_session()
        
    except Exception as e:
        print(f"\n❌ Critical test error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await tester.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 AUTHENTICATION TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    # Group results by category
    basic_auth_tests = ['register', 'login', 'get_me']
    password_reset_tests = ['forgot_password', 'reset_password', 'login_new_password']
    oauth_tests = ['google_oauth_missing', 'google_oauth_invalid']
    
    print("\n🔐 Basic Authentication:")
    for test_name in basic_auth_tests:
        if test_name in test_results:
            status = "✅ PASS" if test_results[test_name] else "❌ FAIL"
            print(f"  {test_name.replace('_', ' ').title():<25} {status}")
    
    print("\n🔑 Password Reset Flow:")
    for test_name in password_reset_tests:
        if test_name in test_results:
            status = "✅ PASS" if test_results[test_name] else "❌ FAIL"
            print(f"  {test_name.replace('_', ' ').title():<25} {status}")
    
    print("\n🔗 Google OAuth Session:")
    for test_name in oauth_tests:
        if test_name in test_results:
            status = "✅ PASS" if test_results[test_name] else "❌ FAIL"
            print(f"  {test_name.replace('_', ' ').title():<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All authentication tests passed! Backend auth system is working correctly.")
    else:
        print("⚠️  Some authentication tests failed. Check the detailed output above.")
    
    return test_results

if __name__ == "__main__":
    asyncio.run(run_auth_tests())