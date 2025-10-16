#!/usr/bin/env python3
"""
Test script to verify Flask backend endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health endpoint"""
    print("\n🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:5000/health")
        print(f"✅ Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_signup():
    """Test signup endpoint"""
    print("\n🔍 Testing signup endpoint...")
    data = {
        "email": "test@example.com",
        "password": "password123",
        "fullName": "Test User"
    }
    try:
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code in [200, 201, 409]:
            print(f"   Response: {response.json()}")
            print(f"   Cookies: {response.cookies}")
            return True
        else:
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_login():
    """Test login endpoint"""
    print("\n🔍 Testing login endpoint...")
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            print(f"   Cookies: {dict(response.cookies)}")
            
            # Test /auth/me with the cookie
            print("\n🔍 Testing /auth/me with cookie...")
            me_response = requests.get(
                f"{BASE_URL}/auth/me",
                cookies=response.cookies
            )
            print(f"✅ /auth/me Status: {me_response.status_code}")
            if me_response.status_code == 200:
                print(f"   User: {me_response.json()}")
            else:
                print(f"   Error: {me_response.text}")
            
            return True
        else:
            print(f"   Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Flask Backend API Tests")
    print("=" * 60)
    
    # Run tests
    test_health()
    test_signup()
    test_login()
    
    print("\n" + "=" * 60)
    print("✅ Tests completed!")
    print("=" * 60)
