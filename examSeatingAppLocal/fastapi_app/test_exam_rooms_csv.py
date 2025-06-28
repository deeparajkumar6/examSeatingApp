#!/usr/bin/env python3
"""
Test script to verify exam room CSV upload functionality
"""

import requests
import os

BASE_URL = "http://localhost:8000"

def test_exam_rooms_csv_upload():
    print("Testing Exam Rooms CSV Upload Functionality...")
    
    # Create a test CSV file
    csv_content = """roomNumber,roomCapacity,roomFloor,roomBuilding
Test Room 1,25,Ground Floor,Test Building A
Test Room 2,30,First Floor,Test Building A
Test Lab A,20,Ground Floor,Test Building B
Test Lab B,22,First Floor,Test Building B
Test Auditorium,100,Ground Floor,Test Building C"""
    
    with open('test_exam_rooms.csv', 'w') as f:
        f.write(csv_content)
    
    try:
        # Test CSV upload
        print("\n1. Testing Exam Rooms CSV Upload")
        with open('test_exam_rooms.csv', 'rb') as f:
            files = {'file': ('test_exam_rooms.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload-exam-rooms-csv", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Exam rooms CSV upload successful!")
            print(f"  Rooms processed: {result['summary']['total_rooms_processed']}")
            print(f"  Rooms added: {result['summary']['rooms_added']}")
            print(f"  Rooms skipped: {result['summary']['rooms_skipped']}")
            print(f"  Errors: {result['summary']['errors_count']}")
        else:
            print(f"✗ Exam rooms CSV upload failed: {response.status_code} - {response.text}")
            return
        
        # Test getting exam rooms to verify upload
        print("\n2. Verifying uploaded exam rooms")
        response = requests.get(f"{BASE_URL}/examRoom")
        if response.status_code == 200:
            rooms = response.json()['examRooms']
            print(f"✓ Found {len(rooms)} exam rooms total")
            
            for room in rooms:
                if room['roomNumber'].startswith('Test'):
                    print(f"  - {room['roomNumber']}: Capacity {room['roomCapacity']}, {room['roomFloor']}, {room['roomBuilding']}")
        
        # Test template download
        print("\n3. Testing exam rooms template download")
        response = requests.get(f"{BASE_URL}/download-exam-rooms-csv-template")
        if response.status_code == 200:
            print("✓ Exam rooms template download successful")
            with open('downloaded_exam_rooms_template.csv', 'wb') as f:
                f.write(response.content)
            print("  Template saved as 'downloaded_exam_rooms_template.csv'")
        else:
            print(f"✗ Exam rooms template download failed: {response.status_code}")
        
        # Test error handling with invalid data
        print("\n4. Testing error handling with invalid data")
        invalid_csv = """roomNumber,roomCapacity,roomFloor,roomBuilding
Invalid Room,not_a_number,Floor 1,Building A
,30,Floor 2,Building B"""
        
        with open('test_invalid_rooms.csv', 'w') as f:
            f.write(invalid_csv)
        
        with open('test_invalid_rooms.csv', 'rb') as f:
            files = {'file': ('test_invalid_rooms.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload-exam-rooms-csv", files=files)
        
        if response.status_code == 400:
            print("✓ Error handling working correctly - invalid data rejected")
        else:
            print(f"⚠️  Expected error for invalid data, got: {response.status_code}")
        
        print("\n🎉 All exam rooms CSV tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
    finally:
        # Clean up test files
        for filename in ['test_exam_rooms.csv', 'test_invalid_rooms.csv', 'downloaded_exam_rooms_template.csv']:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    test_exam_rooms_csv_upload()
