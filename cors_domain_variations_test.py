#!/usr/bin/env python3
"""
CORS Domain Variations Test for videopromt.com
Tests all videopromt.com domain variations configured in CORS_ORIGINS
"""

import asyncio
import httpx
import time

# Configuration
BACKEND_URL = "https://c-project-4.preview.emergentagent.com"
API_BASE = f"{BACKEND_URL}/api"

# Test all videopromt.com variations from CORS_ORIGINS
DOMAIN_VARIATIONS = [
    "http://videopromt.com",
    "https://videopromt.com", 
    "http://www.videopromt.com",
    "https://www.videopromt.com"
]

class CORSDomainTester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def test_domain_cors(self, origin):
        """Test CORS for a specific domain origin"""
        print(f"\n🌐 Testing CORS for: {origin}")
        
        try:
            # Test OPTIONS preflight
            response = await self.client.options(
                f"{API_BASE}/auth/login",
                headers={
                    "Origin": origin,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "Content-Type"
                }
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                allowed_origin = response.headers.get("Access-Control-Allow-Origin")
                allow_credentials = response.headers.get("Access-Control-Allow-Credentials")
                
                print(f"   Access-Control-Allow-Origin: {allowed_origin}")
                print(f"   Access-Control-Allow-Credentials: {allow_credentials}")
                
                if allowed_origin == origin or allowed_origin == "*":
                    print(f"   ✅ CORS working for {origin}")
                    return True
                else:
                    print(f"   ❌ CORS not configured for {origin}")
                    return False
            else:
                print(f"   ❌ CORS preflight failed with status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error testing {origin}: {e}")
            return False
    
    async def test_login_with_domain(self, origin):
        """Test actual login with domain origin"""
        print(f"\n🔐 Testing Login with: {origin}")
        
        # Use domain-specific email to avoid collisions
        domain_safe = origin.replace("://", "_").replace(".", "_").replace("/", "_")
        test_email = f"domaintest{int(time.time())}_{domain_safe}@example.com"
        
        try:
            # First register a user
            reg_response = await self.client.post(
                f"{API_BASE}/auth/register",
                json={
                    "email": test_email,
                    "password": "TestPass123!",
                    "name": "Domain Test User"
                },
                headers={
                    "Origin": origin,
                    "Content-Type": "application/json"
                }
            )
            
            if reg_response.status_code != 200:
                print(f"   ❌ Registration failed: {reg_response.text}")
                return False
            
            # Then test login
            login_response = await self.client.post(
                f"{API_BASE}/auth/login",
                json={
                    "email": test_email,
                    "password": "TestPass123!"
                },
                headers={
                    "Origin": origin,
                    "Content-Type": "application/json"
                }
            )
            
            print(f"   Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                cors_origin = login_response.headers.get("Access-Control-Allow-Origin")
                data = login_response.json()
                
                print(f"   Access-Control-Allow-Origin: {cors_origin}")
                print(f"   Access token received: {'✅ Yes' if data.get('access_token') else '❌ No'}")
                
                if cors_origin == origin or cors_origin == "*":
                    print(f"   ✅ Login working with CORS for {origin}")
                    return True
                else:
                    print(f"   ❌ CORS headers incorrect for {origin}")
                    return False
            else:
                print(f"   ❌ Login failed: {login_response.text}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error testing login with {origin}: {e}")
            return False
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

async def run_domain_variations_test():
    """Test all videopromt.com domain variations"""
    print("🚀 Testing CORS for All videopromt.com Domain Variations")
    print("=" * 70)
    print(f"Backend URL: {BACKEND_URL}")
    print("=" * 70)
    
    tester = CORSDomainTester()
    results = {}
    
    try:
        for domain in DOMAIN_VARIATIONS:
            # Test CORS preflight
            cors_result = await tester.test_domain_cors(domain)
            
            # Test actual login
            login_result = await tester.test_login_with_domain(domain)
            
            results[domain] = {
                'cors': cors_result,
                'login': login_result,
                'overall': cors_result and login_result
            }
            
    except Exception as e:
        print(f"\n❌ Critical test error: {e}")
    
    finally:
        await tester.close()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 DOMAIN VARIATIONS TEST SUMMARY")
    print("=" * 70)
    
    for domain, result in results.items():
        cors_status = "✅" if result['cors'] else "❌"
        login_status = "✅" if result['login'] else "❌"
        overall_status = "✅ PASS" if result['overall'] else "❌ FAIL"
        
        print(f"{domain:<35} CORS: {cors_status} Login: {login_status} {overall_status}")
    
    total_passed = sum(1 for r in results.values() if r['overall'])
    total_domains = len(results)
    
    print(f"\nOverall: {total_passed}/{total_domains} domains working correctly")
    
    if total_passed == total_domains:
        print("🎉 All videopromt.com domain variations working correctly!")
    else:
        print("⚠️  Some domain variations have issues.")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_domain_variations_test())