#!/usr/bin/env python3
"""
Test script to verify shift field validation in the exam seating app
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_create_class_without_shift():
    """Test creating a class without shift - should fail"""
    print("Testing class creation without shift...")
    
    class_data = {
        "className": "Test Class Without Shift",
        "shift": "",  # Empty shift
        "students": []
    }
    
    response = requests.post(f"{API_BASE}/class", json=class_data)
    
    if response.status_code == 400:
        print("✅ PASS: Class creation without shift correctly rejected")
        print(f"   Error message: {response.json().get('detail', 'No detail')}")
    else:
        print("❌ FAIL: Class creation without shift should have been rejected")
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text}")

def test_create_class_with_shift():
    """Test creating a class with shift - should succeed"""
    print("\nTesting class creation with shift...")
    
    class_data = {
        "className": "Test Class With Shift",
        "shift": "Morning",
        "students": [
            {
                "studentName": "Test Student",
                "language": "English",
                "dateOfBirth": "2000-01-01"
            }
        ]
    }
    
    response = requests.post(f"{API_BASE}/class", json=class_data)
    
    if response.status_code == 200:
        print("✅ PASS: Class creation with shift succeeded")
    else:
        print("❌ FAIL: Class creation with shift should have succeeded")
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text}")

def test_get_classes_with_shift_display():
    """Test getting classes to verify shift is displayed"""
    print("\nTesting class retrieval with shift display...")
    
    response = requests.get(f"{API_BASE}/class")
    
    if response.status_code == 200:
        data = response.json()
        classes = data.get('classes', [])
        
        if classes:
            print("✅ PASS: Classes retrieved successfully")
            for cls in classes:
                shift_text = f" - Shift {cls['shift']}" if cls.get('shift') else " (No shift)"
                print(f"   Class: {cls['className']}{shift_text}")
        else:
            print("ℹ️  INFO: No classes found in database")
    else:
        print("❌ FAIL: Failed to retrieve classes")
        print(f"   Status code: {response.status_code}")
        print(f"   Response: {response.text}")

def main():
    """Run all tests"""
    print("🧪 Testing Shift Field Validation")
    print("=" * 40)
    
    try:
        # Test validation
        test_create_class_without_shift()
        test_create_class_with_shift()
        test_get_classes_with_shift_display()
        
        print("\n" + "=" * 40)
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the API server")
        print("   Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ ERROR: Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
