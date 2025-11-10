#!/usr/bin/env python3
"""
CORS JWT Authentication Testing for videopromt.com domain
Tests CORS preflight, registration, login, and protected endpoints with videopromt.com origin
"""

import asyncio
import httpx
import json
import time
import os
from datetime import datetime

# Configuration - Use the actual backend URL from frontend/.env
BACKEND_URL = "https://core.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"
VIDEOPROMT_ORIGIN = "https://videopromt.com"

class CORSJWTTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.access_token = None
        self.test_email = f"corstest{int(time.time())}@videopromt.com"
        self.test_password = "SecurePass123!"
        
    async def test_cors_preflight_login(self):
        """Test CORS preflight for /api/auth/login with videopromt.com origin"""
        print("\n🌐 Testing CORS Preflight - OPTIONS /api/auth/login")
        print(f"   Origin: {VIDEOPROMT_ORIGIN}")
        
        try:
            response = await self.client.options(
                f"{API_BASE}/auth/login",
                headers={
                    "Origin": VIDEOPROMT_ORIGIN,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            print(f"Status: {response.status_code}")
            
            # Check CORS headers
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
                "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials")
            }
            
            print("   CORS Headers:")
            for header, value in cors_headers.items():
                print(f"     {header}: {value}")
            
            if response.status_code == 200:
                # Verify videopromt.com is allowed
                allowed_origin = cors_headers["Access-Control-Allow-Origin"]
                if allowed_origin == VIDEOPROMT_ORIGIN or allowed_origin == "*":
                    print(f"✅ CORS preflight successful - videopromt.com origin allowed")
                    return True
                else:
                    print(f"❌ CORS preflight failed - videopromt.com origin not allowed")
                    return False
            else:
                print(f"❌ CORS preflight failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ CORS preflight test error: {e}")
            return False
    
    async def test_registration_with_cors(self):
        """Test POST /api/auth/register with videopromt.com origin"""
        print(f"\n🔐 Testing Registration with CORS - POST /api/auth/register")
        print(f"   Origin: {VIDEOPROMT_ORIGIN}")
        print(f"   Email: {self.test_email}")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/register",
                json={
                    "email": self.test_email,
                    "password": self.test_password,
                    "name": "CORS Test User"
                },
                headers={
                    "Origin": VIDEOPROMT_ORIGIN,
                    "Content-Type": "application/json"
                }
            )
            
            print(f"Status: {response.status_code}")
            
            # Check CORS headers in response
            cors_origin = response.headers.get("Access-Control-Allow-Origin")
            cors_credentials = response.headers.get("Access-Control-Allow-Credentials")
            
            print(f"   Access-Control-Allow-Origin: {cors_origin}")
            print(f"   Access-Control-Allow-Credentials: {cors_credentials}")
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token")
                
                print(f"✅ Registration successful with CORS headers")
                print(f"   Access token received: {'✅ Yes' if self.access_token else '❌ No'}")
                print(f"   User ID: {data.get('user', {}).get('id')}")
                
                # Verify CORS headers
                if cors_origin in [VIDEOPROMT_ORIGIN, "*"]:
                    print(f"✅ CORS headers correct for videopromt.com")
                    return True
                else:
                    print(f"❌ CORS headers missing or incorrect")
                    return False
            else:
                print(f"❌ Registration failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Registration with CORS test error: {e}")
            return False
    
    async def test_login_with_cors(self):
        """Test POST /api/auth/login with videopromt.com origin"""
        print(f"\n🔐 Testing Login with CORS - POST /api/auth/login")
        print(f"   Origin: {VIDEOPROMT_ORIGIN}")
        print(f"   Email: {self.test_email}")
        
        try:
            response = await self.client.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": self.test_email,
                    "password": self.test_password
                },
                headers={
                    "Origin": VIDEOPROMT_ORIGIN,
                    "Content-Type": "application/json"
                }
            )
            
            print(f"Status: {response.status_code}")
            
            # Check CORS headers in response
            cors_origin = response.headers.get("Access-Control-Allow-Origin")
            cors_credentials = response.headers.get("Access-Control-Allow-Credentials")
            
            print(f"   Access-Control-Allow-Origin: {cors_origin}")
            print(f"   Access-Control-Allow-Credentials: {cors_credentials}")
            
            if response.status_code == 200:
                data = response.json()
                login_token = data.get("access_token")
                user_data = data.get("user", {})
                
                print(f"✅ Login successful with CORS headers")
                print(f"   Access token received: {'✅ Yes' if login_token else '❌ No'}")
                print(f"   User ID: {user_data.get('id')}")
                print(f"   User email: {user_data.get('email')}")
                print(f"   Subscription plan: {user_data.get('subscription_plan')}")
                
                # Update token for protected endpoint test
                if login_token:
                    self.access_token = login_token
                
                # Verify CORS headers
                if cors_origin in [VIDEOPROMT_ORIGIN, "*"]:
                    print(f"✅ CORS headers correct for videopromt.com")
                    return True
                else:
                    print(f"❌ CORS headers missing or incorrect")
                    return False
            else:
                print(f"❌ Login failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Login with CORS test error: {e}")
            return False
    
    async def test_protected_endpoint_with_cors(self):
        """Test GET /api/auth/me with Bearer token and videopromt.com origin"""
        print(f"\n🔐 Testing Protected Endpoint with CORS - GET /api/auth/me")
        print(f"   Origin: {VIDEOPROMT_ORIGIN}")
        print(f"   Bearer token: {'✅ Available' if self.access_token else '❌ Missing'}")
        
        if not self.access_token:
            print("❌ No access token available for protected endpoint test")
            return False
        
        try:
            response = await self.client.get(
                f"{API_BASE}/auth/me",
                headers={
                    "Origin": VIDEOPROMT_ORIGIN,
                    "Authorization": f"Bearer {self.access_token}"
                }
            )
            
            print(f"Status: {response.status_code}")
            
            # Check CORS headers in response
            cors_origin = response.headers.get("Access-Control-Allow-Origin")
            cors_credentials = response.headers.get("Access-Control-Allow-Credentials")
            
            print(f"   Access-Control-Allow-Origin: {cors_origin}")
            print(f"   Access-Control-Allow-Credentials: {cors_credentials}")
            
            if response.status_code == 200:
                user_data = response.json()
                
                print(f"✅ Protected endpoint access successful with CORS headers")
                print(f"   User ID: {user_data.get('id')}")
                print(f"   Email: {user_data.get('email')}")
                print(f"   Name: {user_data.get('name')}")
                print(f"   Videos created: {user_data.get('videos_created', 0)}")
                
                # Verify CORS headers
                if cors_origin in [VIDEOPROMT_ORIGIN, "*"]:
                    print(f"✅ CORS headers correct for videopromt.com")
                    return True
                else:
                    print(f"❌ CORS headers missing or incorrect")
                    return False
            else:
                print(f"❌ Protected endpoint access failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Protected endpoint with CORS test error: {e}")
            return False
    
    async def test_cors_preflight_protected(self):
        """Test CORS preflight for /api/auth/me with videopromt.com origin"""
        print("\n🌐 Testing CORS Preflight for Protected Endpoint - OPTIONS /api/auth/me")
        print(f"   Origin: {VIDEOPROMT_ORIGIN}")
        
        try:
            response = await self.client.options(
                f"{API_BASE}/auth/me",
                headers={
                    "Origin": VIDEOPROMT_ORIGIN,
                    "Access-Control-Request-Method": "GET",
                    "Access-Control-Request-Headers": "Authorization"
                }
            )
            
            print(f"Status: {response.status_code}")
            
            # Check CORS headers
            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
                "Access-Control-Allow-Credentials": response.headers.get("Access-Control-Allow-Credentials")
            }
            
            print("   CORS Headers:")
            for header, value in cors_headers.items():
                print(f"     {header}: {value}")
            
            if response.status_code == 200:
                # Verify videopromt.com is allowed and Authorization header is allowed
                allowed_origin = cors_headers["Access-Control-Allow-Origin"]
                allowed_headers = cors_headers["Access-Control-Allow-Headers"] or ""
                
                origin_ok = allowed_origin == VIDEOPROMT_ORIGIN or allowed_origin == "*"
                auth_header_ok = "authorization" in allowed_headers.lower() or "*" in allowed_headers
                
                if origin_ok and auth_header_ok:
                    print(f"✅ CORS preflight for protected endpoint successful")
                    return True
                else:
                    print(f"❌ CORS preflight failed - origin_ok: {origin_ok}, auth_header_ok: {auth_header_ok}")
                    return False
            else:
                print(f"❌ CORS preflight failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ CORS preflight for protected endpoint test error: {e}")
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_cors_jwt_tests():
    """Run all CORS JWT tests for videopromt.com domain"""
    print("🚀 Starting CORS JWT Authentication Tests for videopromt.com")
    print("=" * 70)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Testing Origin: {VIDEOPROMT_ORIGIN}")
    print("=" * 70)
    
    tester = CORSJWTTester()
    test_results = {}
    
    try:
        # Test sequence as requested
        test_results['cors_preflight_login'] = await tester.test_cors_preflight_login()
        test_results['registration_with_cors'] = await tester.test_registration_with_cors()
        test_results['login_with_cors'] = await tester.test_login_with_cors()
        test_results['cors_preflight_protected'] = await tester.test_cors_preflight_protected()
        test_results['protected_endpoint_with_cors'] = await tester.test_protected_endpoint_with_cors()
        
    except Exception as e:
        print(f"\n❌ Critical test error: {e}")
    
    finally:
        await tester.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 CORS JWT TEST RESULTS SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():<40} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All CORS JWT tests passed! videopromt.com authentication working correctly.")
    else:
        print("⚠️  Some CORS JWT tests failed. Check the detailed output above.")
        print("\n🔍 TROUBLESHOOTING:")
        print("   - Verify CORS_ORIGINS includes videopromt.com domains in backend/.env")
        print("   - Check if backend service is running and accessible")
        print("   - Ensure CORS middleware is properly configured in FastAPI")
    
    return test_results

if __name__ == "__main__":
    asyncio.run(run_cors_jwt_tests())