#!/usr/bin/env python3
"""
Test script to verify CSV upload functionality
"""

import requests
import os

BASE_URL = "http://localhost:8000"

def test_csv_upload():
    print("Testing CSV Upload Functionality...")
    
    # Create a test CSV file
    csv_content = """className,rollNumber,studentName
Test Class 1,T101,Student One
Test Class 1,T103,Student Three
Test Class 1,T105,Student Five
Test Class 2,T201,Student Alpha
Test Class 2,T203,Student Beta
Test Class 2,T205,Student Gamma"""
    
    with open('test_upload.csv', 'w') as f:
        f.write(csv_content)
    
    try:
        # Test CSV upload
        print("\n1. Testing CSV Upload")
        with open('test_upload.csv', 'rb') as f:
            files = {'file': ('test_upload.csv', f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/upload-csv", files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✓ CSV upload successful!")
            print(f"  Students processed: {result['summary']['total_students_processed']}")
            print(f"  Classes created: {result['summary']['classes_created']}")
            print(f"  Classes updated: {result['summary']['classes_updated']}")
            print(f"  Errors: {result['summary']['errors_count']}")
            
            if result['details']['created_classes']:
                print(f"  Created classes: {', '.join(result['details']['created_classes'])}")
        else:
            print(f"✗ CSV upload failed: {response.status_code} - {response.text}")
            return
        
        # Test getting classes to verify upload
        print("\n2. Verifying uploaded data")
        response = requests.get(f"{BASE_URL}/class")
        if response.status_code == 200:
            classes = response.json()['classes']
            print(f"✓ Found {len(classes)} classes total")
            
            for cls in classes:
                if cls['className'].startswith('Test Class'):
                    print(f"  - {cls['className']}: {len(cls['students'])} students")
                    for student in cls['students']:
                        print(f"    * {student['rollNumber']}: {student['studentName']}")
        
        # Test template download
        print("\n3. Testing template download")
        response = requests.get(f"{BASE_URL}/download-csv-template")
        if response.status_code == 200:
            print("✓ Template download successful")
            with open('downloaded_template.csv', 'wb') as f:
                f.write(response.content)
            print("  Template saved as 'downloaded_template.csv'")
        else:
            print(f"✗ Template download failed: {response.status_code}")
        
        print("\n🎉 All CSV tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
    finally:
        # Clean up test files
        for filename in ['test_upload.csv', 'downloaded_template.csv']:
            if os.path.exists(filename):
                os.remove(filename)

if __name__ == "__main__":
    test_csv_upload()
