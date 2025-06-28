#!/usr/bin/env python3
"""
Comprehensive test script for both student and exam room CSV upload functionality
"""

import requests
import os

BASE_URL = "http://localhost:8000"

def test_all_csv_functionality():
    print("🧪 Testing Complete CSV Upload Functionality")
    print("=" * 50)
    
    # Test data
    students_csv = """className,rollNumber,studentName
Test Class Alpha,TA101,Alice Test
Test Class Alpha,TA103,Bob Test
Test Class Alpha,TA105,Charlie Test
Test Class Beta,TB201,Diana Test
Test Class Beta,TB203,Eve Test"""

    rooms_csv = """roomNumber,roomCapacity,roomFloor,roomBuilding
Test Room A1,25,Ground Floor,Test Building A
Test Room A2,30,First Floor,Test Building A
Test Lab B1,20,Ground Floor,Test Building B
Test Auditorium C1,100,Ground Floor,Test Building C"""

    try:
        # 1. Test Student CSV Upload
        print("\n📚 Testing Student CSV Upload")
        print("-" * 30)
        
        with open('test_students.csv', 'w') as f:
            f.write(students_csv)
        
        with open('test_students.csv', 'rb') as f:
            files = {'file': ('test_students.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload-csv", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Student CSV upload successful!")
            print(f"   📊 Students processed: {result['summary']['total_students_processed']}")
            print(f"   🆕 Classes created: {result['summary']['classes_created']}")
            print(f"   📝 Classes updated: {result['summary']['classes_updated']}")
            print(f"   ⚠️  Errors: {result['summary']['errors_count']}")
        else:
            print(f"❌ Student CSV upload failed: {response.status_code}")
            return False

        # 2. Test Exam Room CSV Upload
        print("\n🏢 Testing Exam Room CSV Upload")
        print("-" * 30)
        
        with open('test_rooms.csv', 'w') as f:
            f.write(rooms_csv)
        
        with open('test_rooms.csv', 'rb') as f:
            files = {'file': ('test_rooms.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload-exam-rooms-csv", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Exam room CSV upload successful!")
            print(f"   📊 Rooms processed: {result['summary']['total_rooms_processed']}")
            print(f"   🆕 Rooms added: {result['summary']['rooms_added']}")
            print(f"   ⏭️  Rooms skipped: {result['summary']['rooms_skipped']}")
            print(f"   ⚠️  Errors: {result['summary']['errors_count']}")
        else:
            print(f"❌ Exam room CSV upload failed: {response.status_code}")
            return False

        # 3. Verify Data Upload
        print("\n🔍 Verifying Uploaded Data")
        print("-" * 30)
        
        # Check classes
        response = requests.get(f"{BASE_URL}/class")
        if response.status_code == 200:
            classes = response.json()['classes']
            test_classes = [c for c in classes if c['className'].startswith('Test Class')]
            print(f"✅ Found {len(test_classes)} test classes:")
            for cls in test_classes:
                print(f"   📚 {cls['className']}: {len(cls['students'])} students")
        
        # Check exam rooms
        response = requests.get(f"{BASE_URL}/examRoom")
        if response.status_code == 200:
            rooms = response.json()['examRooms']
            test_rooms = [r for r in rooms if r['roomNumber'].startswith('Test')]
            print(f"✅ Found {len(test_rooms)} test exam rooms:")
            for room in test_rooms:
                print(f"   🏢 {room['roomNumber']}: Capacity {room['roomCapacity']}")

        # 4. Test Template Downloads
        print("\n📥 Testing Template Downloads")
        print("-" * 30)
        
        # Student template
        response = requests.get(f"{BASE_URL}/download-csv-template")
        if response.status_code == 200:
            print("✅ Student template download successful")
        else:
            print("❌ Student template download failed")
        
        # Exam room template
        response = requests.get(f"{BASE_URL}/download-exam-rooms-csv-template")
        if response.status_code == 200:
            print("✅ Exam room template download successful")
        else:
            print("❌ Exam room template download failed")

        # 5. Test Scheduling with Uploaded Data
        print("\n📅 Testing Scheduling with Uploaded Data")
        print("-" * 30)
        
        # Get test class and room IDs
        classes_response = requests.get(f"{BASE_URL}/class")
        rooms_response = requests.get(f"{BASE_URL}/examRoom")
        
        if classes_response.status_code == 200 and rooms_response.status_code == 200:
            classes = classes_response.json()['classes']
            rooms = rooms_response.json()['examRooms']
            
            test_class_ids = [c['id'] for c in classes if c['className'].startswith('Test Class')]
            test_room_ids = [r['id'] for r in rooms if r['roomNumber'].startswith('Test')]
            
            if test_class_ids and test_room_ids:
                schedule_data = {
                    "date": "2024-12-15",
                    "classes": test_class_ids[:2],  # Use first 2 test classes
                    "exam_rooms": test_room_ids[:2],  # Use first 2 test rooms
                    "split": True
                }
                
                response = requests.post(f"{BASE_URL}/schedule", json=schedule_data)
                if response.status_code == 200:
                    result = response.json()
                    print("✅ Scheduling with uploaded data successful!")
                    print(f"   📅 Date: {result['date']}")
                    for room, students in result['seating_arrangement'].items():
                        print(f"   🏢 {room}: {len(students)} students")
                else:
                    print(f"❌ Scheduling failed: {response.status_code}")
            else:
                print("⚠️  No test data available for scheduling")

        print("\n🎉 All CSV functionality tests completed successfully!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    finally:
        # Clean up test files
        for filename in ['test_students.csv', 'test_rooms.csv']:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    success = test_all_csv_functionality()
    if success:
        print("\n✨ All tests passed! CSV upload functionality is working correctly.")
    else:
        print("\n💥 Some tests failed. Please check the API server and try again.")
