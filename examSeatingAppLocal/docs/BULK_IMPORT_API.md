# Bulk Import API Documentation

## Overview

The Bulk Import API allows you to upload Excel files containing student data and automatically create classes with students. The API supports the specific Excel format used in your institution.

## New Features Added

### Database Schema Updates
- **Classes table**: Added `shift` field
- **Students table**: Added `language` and `dateOfBirth` fields

### API Endpoints

#### 1. Bulk Import Excel File
**POST** `/bulk-import/excel`

Upload an Excel file to create classes and students in bulk.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Excel file (.xlsx or .xls)

**Response:**
```json
{
  "message": "Successfully imported 1 classes with 5 students",
  "classesCreated": 1,
  "studentsCreated": 5,
  "details": [
    {
      "className": "I B.COM -CS",
      "shift": "I",
      "action": "created",
      "studentsAdded": 5
    }
  ]
}
```

#### 2. Validate Excel File
**POST** `/bulk-import/validate`

Validate an Excel file without importing the data.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Excel file (.xlsx or .xls)

**Response:**
```json
{
  "valid": true,
  "errors": [],
  "summary": {
    "academic_year": "I YEAR 2023-24",
    "total_classes": 1,
    "total_students": 5,
    "classes": [
      {
        "class_name": "I B.COM -CS",
        "shift": "I",
        "student_count": 5
      }
    ]
  }
}
```

#### 3. Get Template Information
**GET** `/bulk-import/template`

Get information about the expected Excel file format.

**Response:**
```json
{
  "message": "Excel template information",
  "format": {
    "description": "Excel file should contain student data in the following format:",
    "structure": [
      "Row 1-3: Empty or metadata",
      "Row 4: Academic year (e.g., 'I YEAR 2023-24')",
      "Row 5: Headers - S.No | Register Number | Names with Date of Birth | Dept/Class | Shift | Language",
      "Row 6+: Student data alternating between:",
      "  - Main row: Serial No | Register No | Student Name | Department | Shift | Language",
      "  - DOB row: Empty | Empty | Date of Birth | Empty | Empty | Empty"
    ]
  }
}
```

## Excel File Format

### Required Structure

1. **Row 4**: Academic year information (e.g., "I YEAR 2023-24")
2. **Row 5**: Column headers:
   - S.No
   - Register Number
   - Names with Date of Birth
   - Dept / Class
   - Shift
   - Language

3. **Data rows**: Student information split across two rows:
   - **Main row**: Serial No, Register Number, Student Name, Department, Shift, Language
   - **DOB row**: Empty, Empty, Date of Birth, Empty, Empty, Empty

### Example Excel Structure

| S.No | Register Number | Names with Date of Birth | Dept / Class | Shift | Language |
|------|----------------|---------------------------|--------------|-------|----------|
| 1    | 122302982      | Amirtha                   | I B.COM -CS  | I     | TAMIL    |
|      |                | 2000-06-22                |              |       |          |
| 2    | 122302983      | Bmirtha                   | I B.COM -CS  | I     | HINDI    |
|      |                | 2001-06-22                |              |       |          |

## Field Mappings

### Class Fields
- `className`: Mapped from "Dept / Class" column
- `shift`: Mapped from "Shift" column (e.g., "I" for first shift)

### Student Fields
- `rollNumber`: Mapped from "Register Number" column
- `studentName`: Mapped from student name in "Names with Date of Birth" column
- `language`: Mapped from "Language" column (optional)
- `dateOfBirth`: Mapped from date in "Names with Date of Birth" column (optional)

## Usage Examples

### Using cURL

1. **Upload Excel file:**
```bash
curl -X POST "http://localhost:8000/bulk-import/excel" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/student_list.xlsx"
```

2. **Validate Excel file:**
```bash
curl -X POST "http://localhost:8000/bulk-import/validate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/student_list.xlsx"
```

### Using Python requests

```python
import requests

# Upload Excel file
with open('student_list.xlsx', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/bulk-import/excel', files=files)
    print(response.json())

# Validate Excel file
with open('student_list.xlsx', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/bulk-import/validate', files=files)
    print(response.json())
```

## Error Handling

### Common Errors

1. **Invalid file type:**
```json
{
  "detail": "Invalid file type. Please upload an Excel file (.xlsx or .xls)"
}
```

2. **Validation errors:**
```json
{
  "detail": "Validation errors: Class 'I B.COM -CS', Student 1: Missing register number"
}
```

3. **Parsing errors:**
```json
{
  "detail": "Error parsing Excel file: Could not find header row in Excel file"
}
```

## Behavior Notes

1. **Duplicate Classes**: If a class with the same name and shift already exists, the students will be updated (old students deleted, new ones added).

2. **Duplicate Students**: Students with duplicate register numbers within the same class will be skipped.

3. **Data Validation**: The API validates:
   - Required fields (register number, student name)
   - Date format for date of birth
   - Duplicate register numbers within classes

4. **Transaction Safety**: All operations are performed within database transactions, so partial failures are rolled back.

## Testing

You can test the functionality using the provided test script:

```bash
python3 test_bulk_import.py
```

This will validate the parsing logic using your sample Excel file without actually importing data to the database.
