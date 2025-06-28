#!/usr/bin/env python3
"""
Test script to verify the API endpoints work correctly
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing Exam Seating App API...")
    
    try:
        # Test getting classes
        print("\n1. Testing GET /class")
        response = requests.get(f"{BASE_URL}/class")
        if response.status_code == 200:
            classes = response.json()
            print(f"✓ Found {len(classes['classes'])} classes")
            for cls in classes['classes']:
                print(f"  - {cls['className']}: {len(cls['students'])} students")
        else:
            print(f"✗ Failed: {response.status_code}")
            return
        
        # Test getting exam rooms
        print("\n2. Testing GET /examRoom")
        response = requests.get(f"{BASE_URL}/examRoom")
        if response.status_code == 200:
            rooms = response.json()
            print(f"✓ Found {len(rooms['examRooms'])} exam rooms")
            for room in rooms['examRooms']:
                print(f"  - {room['roomNumber']}: Capacity {room['roomCapacity']}")
        else:
            print(f"✗ Failed: {response.status_code}")
            return
        
        # Test creating a new class
        print("\n3. Testing POST /class")
        new_class = {
            "className": "Test Class B",
            "students": [
                {"rollNumber": "201", "studentName": "Alice"},
                {"rollNumber": "203", "studentName": "Bob"},
                {"rollNumber": "205", "studentName": "Charlie"}
            ]
        }
        response = requests.post(f"{BASE_URL}/class", json=new_class)
        if response.status_code == 200:
            print("✓ Class created successfully")
        else:
            print(f"✗ Failed: {response.status_code} - {response.text}")
            return
        
        # Test scheduling
        print("\n4. Testing POST /schedule")
        schedule_data = {
            "date": "2024-12-01",
            "classes": [1, 2],  # Assuming we have at least 2 classes now
            "exam_rooms": [1],  # Assuming we have at least 1 room
            "split": False
        }
        response = requests.post(f"{BASE_URL}/schedule", json=schedule_data)
        if response.status_code == 200:
            result = response.json()
            print("✓ Schedule generated successfully")
            print(f"  Date: {result['date']}")
            for room, students in result['seating_arrangement'].items():
                print(f"  {room}: {len(students)} students")
        else:
            print(f"✗ Failed: {response.status_code} - {response.text}")
        
        print("\n🎉 All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"✗ Test failed with error: {e}")

if __name__ == "__main__":
    test_api()
