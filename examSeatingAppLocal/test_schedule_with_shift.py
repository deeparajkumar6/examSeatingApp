#!/usr/bin/env python3
"""
Test script to verify schedule response includes shift information
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def create_test_class(class_name, shift):
    """Create a test class with shift"""
    class_data = {
        "className": class_name,
        "shift": shift,
        "students": [
            {
                "studentName": f"Student 1 from {class_name}",
                "language": "English",
                "dateOfBirth": "2000-01-01"
            },
            {
                "studentName": f"Student 2 from {class_name}",
                "language": "English", 
                "dateOfBirth": "2000-01-02"
            }
        ]
    }
    
    response = requests.post(f"{API_BASE}/class", json=class_data)
    if response.status_code == 200:
        print(f"✅ Created class: {class_name} - {shift}")
        return True
    else:
        print(f"❌ Failed to create class: {class_name} - {shift}")
        print(f"   Error: {response.text}")
        return False

def create_test_room(room_number, capacity):
    """Create a test exam room"""
    room_data = {
        "roomNumber": room_number,
        "roomCapacity": capacity,
        "roomFloor": "Ground Floor",
        "roomBuilding": "Main Building"
    }
    
    response = requests.post(f"{API_BASE}/exam-room", json=room_data)
    if response.status_code == 200:
        print(f"✅ Created room: {room_number} (capacity: {capacity})")
        return True
    else:
        print(f"❌ Failed to create room: {room_number}")
        print(f"   Error: {response.text}")
        return False

def get_classes():
    """Get all classes and return their IDs"""
    response = requests.get(f"{API_BASE}/class")
    if response.status_code == 200:
        data = response.json()
        classes = data.get('classes', [])
        return [(cls['id'], cls['className'], cls.get('shift', '')) for cls in classes]
    return []

def get_exam_rooms():
    """Get all exam rooms and return their IDs"""
    response = requests.get(f"{API_BASE}/exam-room")
    if response.status_code == 200:
        data = response.json()
        rooms = data.get('exam_rooms', [])
        return [(room['id'], room['roomNumber']) for room in rooms]
    return []

def test_schedule_with_shift():
    """Test schedule generation with shift information"""
    print("\n🧪 Testing Schedule Generation with Shift Information")
    print("=" * 60)
    
    # Create test classes with different shifts
    print("\n1. Creating test classes...")
    create_test_class("Computer Science", "Morning")
    create_test_class("Electronics", "Evening")
    create_test_class("Mechanical", "I")
    
    # Create test rooms
    print("\n2. Creating test rooms...")
    create_test_room("Room-101", 10)
    create_test_room("Room-102", 8)
    
    # Get class and room IDs
    classes = get_classes()
    rooms = get_exam_rooms()
    
    if not classes or not rooms:
        print("❌ No classes or rooms available for testing")
        return
    
    print(f"\n3. Available classes:")
    for class_id, class_name, shift in classes:
        print(f"   ID: {class_id}, Name: {class_name}, Shift: {shift}")
    
    print(f"\n4. Available rooms:")
    for room_id, room_number in rooms:
        print(f"   ID: {room_id}, Number: {room_number}")
    
    # Create schedule request
    schedule_data = {
        "date": "2024-12-15",
        "classes": [cls[0] for cls in classes[:2]],  # Use first 2 classes
        "exam_rooms": [room[0] for room in rooms[:2]],  # Use first 2 rooms
        "split": True
    }
    
    print(f"\n5. Creating schedule...")
    print(f"   Classes: {[cls[1] + ' - ' + cls[2] for cls in classes[:2]]}")
    print(f"   Rooms: {[room[1] for room in rooms[:2]]}")
    
    response = requests.post(f"{API_BASE}/schedule", json=schedule_data)
    
    if response.status_code == 200:
        schedule_result = response.json()
        print("✅ Schedule created successfully!")
        
        # Analyze the response
        print("\n6. Schedule Analysis:")
        print(f"   Date: {schedule_result.get('date')}")
        
        seating_arrangement = schedule_result.get('seating_arrangement', {})
        class_summary = schedule_result.get('class_summary', {})
        class_info = schedule_result.get('class_info', {})
        
        print(f"   Rooms scheduled: {len(seating_arrangement)}")
        
        for room_number, students in seating_arrangement.items():
            print(f"\n   📍 {room_number}:")
            print(f"      Students: {len(students)}")
            
            # Group students by class (with shift)
            class_groups = {}
            for student in students:
                if isinstance(student, dict):
                    class_name = student.get('className', 'Unknown')
                    roll_number = student.get('rollNumber', 'Unknown')
                    
                    if class_name not in class_groups:
                        class_groups[class_name] = []
                    class_groups[class_name].append(roll_number)
                else:
                    # Handle old format
                    if 'Unknown' not in class_groups:
                        class_groups['Unknown'] = []
                    class_groups['Unknown'].append(str(student))
            
            for class_name, roll_numbers in class_groups.items():
                print(f"      📚 {class_name}: {len(roll_numbers)} students")
                print(f"         Roll Numbers: {', '.join(roll_numbers)}")
        
        # Check if shift information is included
        shift_info_found = False
        for room_number, students in seating_arrangement.items():
            for student in students:
                if isinstance(student, dict) and student.get('className'):
                    class_name = student.get('className', '')
                    if ' - ' in class_name:
                        shift_info_found = True
                        break
            if shift_info_found:
                break
        
        if shift_info_found:
            print("\n✅ PASS: Shift information is included in class names!")
        else:
            print("\n❌ FAIL: Shift information is NOT included in class names")
        
        # Display class summary if available
        if class_summary:
            print(f"\n7. Class Summary per Room:")
            for room, classes in class_summary.items():
                print(f"   {room}: {classes}")
        
        # Display class info if available
        if class_info:
            print(f"\n8. Class Information:")
            for class_id, info in class_info.items():
                print(f"   Class ID {class_id}: {info}")
        
    else:
        print("❌ Failed to create schedule")
        print(f"   Status code: {response.status_code}")
        print(f"   Error: {response.text}")

def main():
    """Run the test"""
    try:
        test_schedule_with_shift()
        print("\n" + "=" * 60)
        print("✅ Test completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the API server")
        print("   Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ ERROR: Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
