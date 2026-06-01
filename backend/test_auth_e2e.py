"""
End-to-end authentication tests.
Tests the complete authentication flow with the API running in Docker.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test that the API is running"""
    print("\n🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    assert response.status_code == 200
    print("   ✅ Health check passed")

def test_login_admin():
    """Test login with admin credentials"""
    print("\n🔍 Testing admin login...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "admin@example.com",
            "password": "admin123"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print(f"   Cookies: {response.cookies.get_dict()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@example.com"
    assert data["role"] == "Manager"
    assert "access_token" in response.cookies
    print("   ✅ Admin login successful")
    return response.cookies

def test_login_employee():
    """Test login with employee credentials"""
    print("\n🔍 Testing employee login...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "employee@example.com",
            "password": "employee123"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print(f"   Cookies: {response.cookies.get_dict()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "employee@example.com"
    assert data["role"] == "Employee"
    assert "access_token" in response.cookies
    print("   ✅ Employee login successful")
    return response.cookies

def test_login_invalid_password():
    """Test login with invalid password"""
    print("\n🔍 Testing login with invalid password...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "admin@example.com",
            "password": "wrongpassword"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    assert response.status_code == 401
    print("   ✅ Invalid password correctly rejected")

def test_login_invalid_email():
    """Test login with non-existent email"""
    print("\n🔍 Testing login with invalid email...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "anypassword"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    assert response.status_code == 401
    print("   ✅ Invalid email correctly rejected")

def test_get_current_user(cookies):
    """Test getting current user info"""
    print("\n🔍 Testing GET /auth/me...")
    response = requests.get(
        f"{BASE_URL}/auth/me",
        cookies=cookies
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "role" in data
    print("   ✅ Current user info retrieved")

def test_get_current_user_unauthenticated():
    """Test getting current user without authentication"""
    print("\n🔍 Testing GET /auth/me without authentication...")
    response = requests.get(f"{BASE_URL}/auth/me")
    print(f"   Status: {response.status_code}")
    
    assert response.status_code == 401
    print("   ✅ Unauthenticated request correctly rejected")

def test_logout(cookies):
    """Test logout"""
    print("\n🔍 Testing logout...")
    response = requests.post(
        f"{BASE_URL}/auth/logout",
        cookies=cookies
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    assert response.status_code == 200
    print("   ✅ Logout successful")
    
    # Try to access protected endpoint after logout
    print("\n🔍 Testing access after logout...")
    response2 = requests.get(
        f"{BASE_URL}/auth/me",
        cookies=response.cookies  # Use cookies after logout (should be cleared)
    )
    print(f"   Status: {response2.status_code}")
    assert response2.status_code == 401
    print("   ✅ Access correctly denied after logout")

def test_api_documentation():
    """Test that API documentation is accessible"""
    print("\n🔍 Testing API documentation...")
    response = requests.get(f"{BASE_URL}/docs")
    print(f"   Status: {response.status_code}")
    assert response.status_code == 200
    print("   ✅ API documentation accessible at http://localhost:8000/docs")

def run_all_tests():
    """Run all authentication tests"""
    print("=" * 70)
    print("🚀 Starting End-to-End Authentication Tests")
    print("=" * 70)
    
    try:
        # Basic tests
        test_health_check()
        test_api_documentation()
        
        # Login tests
        admin_cookies = test_login_admin()
        employee_cookies = test_login_employee()
        test_login_invalid_password()
        test_login_invalid_email()
        
        # Protected endpoint tests
        test_get_current_user(admin_cookies)
        test_get_current_user_unauthenticated()
        
        # Logout test
        test_logout(admin_cookies)
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\n📊 Test Summary:")
        print("   ✅ Health check")
        print("   ✅ API documentation accessible")
        print("   ✅ Admin login")
        print("   ✅ Employee login")
        print("   ✅ Invalid password rejection")
        print("   ✅ Invalid email rejection")
        print("   ✅ Get current user (authenticated)")
        print("   ✅ Unauthenticated request rejection")
        print("   ✅ Logout and cookie clearing")
        print("\n🎉 Phase 1: Authentication Infrastructure - COMPLETE!")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the API at http://localhost:8000")
        print("   Make sure Docker containers are running: docker-compose up -d")
        raise

if __name__ == "__main__":
    run_all_tests()
