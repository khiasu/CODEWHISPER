#!/usr/bin/env python3
"""
Test script for Code Whisper backend
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_modes_endpoint():
    """Test the modes endpoint"""
    print("\n🔍 Testing modes endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/modes")
        if response.status_code == 200:
            print("✅ Modes endpoint passed")
            data = response.json()
            print(f"   Available modes: {data['modes']}")
        else:
            print(f"❌ Modes endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Modes endpoint error: {e}")

def test_explain_endpoint():
    """Test the explain endpoint with sample code"""
    print("\n🔍 Testing explain endpoint...")
    
    # Sample code to test
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
    
    # Test each mode
    modes = ["friend", "professor", "senior", "babysitter"]
    
    for mode in modes:
        print(f"\n   Testing mode: {mode}")
        try:
            payload = {
                "code": test_code,
                "mode": mode
            }
            
            response = requests.post(
                f"{BASE_URL}/explain",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {mode} mode: Success")
                print(f"      Explanation length: {len(data['explanation'])} chars")
            else:
                print(f"   ❌ {mode} mode failed: {response.status_code}")
                print(f"      Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ {mode} mode error: {e}")

def test_error_cases():
    """Test error handling"""
    print("\n🔍 Testing error cases...")
    
    # Test empty code
    print("   Testing empty code...")
    try:
        response = requests.post(
            f"{BASE_URL}/explain",
            json={"code": "", "mode": "friend"}
        )
        if response.status_code == 400:
            print("   ✅ Empty code validation works")
        else:
            print(f"   ❌ Empty code should return 400, got {response.status_code}")
    except Exception as e:
        print(f"   ❌ Empty code test error: {e}")
    
    # Test invalid mode
    print("   Testing invalid mode...")
    try:
        response = requests.post(
            f"{BASE_URL}/explain",
            json={"code": "print('hello')", "mode": "invalid"}
        )
        if response.status_code == 400:
            print("   ✅ Invalid mode validation works")
        else:
            print(f"   ❌ Invalid mode should return 400, got {response.status_code}")
    except Exception as e:
        print(f"   ❌ Invalid mode test error: {e}")

if __name__ == "__main__":
    print("🧪 Code Whisper Backend Test Suite")
    print("=" * 50)
    
    test_health_check()
    test_modes_endpoint()
    test_explain_endpoint()
    test_error_cases()
    
    print("\n🏁 Test suite completed!")
    print("\nNote: If explain endpoint tests fail, make sure:")
    print("1. Ollama is running (ollama serve)")
    print("2. CodeLLaMA model is installed (ollama pull codellama)")
    print("3. Backend server is running (python app.py)")
