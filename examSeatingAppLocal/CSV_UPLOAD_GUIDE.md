# CSV Upload Guide

## Overview
The Exam Seating App supports bulk import of both students and exam rooms via CSV file upload. This feature allows you to quickly add multiple students across different classes and set up exam rooms in a single operation.

## Student CSV Upload

### Required Columns
Your CSV file must contain exactly these three columns (case-sensitive):
- `className` - The name of the class
- `rollNumber` - The student's roll number
- `studentName` - The student's name (can be empty)

### Student CSV Format Example

```csv
className,rollNumber,studentName
Computer Science A,CS101,Alice Johnson
Computer Science A,CS103,Bob Smith
Computer Science A,CS105,Charlie Brown
Mathematics B,MATH201,Eve Wilson
Mathematics B,MATH203,Frank Miller
Physics C,PHY301,Ivy Chen
```

### Student Upload Features
- **Automatic Class Creation**: Creates new classes or adds to existing ones
- **Duplicate Handling**: Skips duplicate students and reports them
- **Missing Roll Numbers**: Supports non-sequential roll numbers
- **Optional Student Names**: Names can be left empty

## Exam Room CSV Upload

### Required Columns
Your CSV file must contain exactly these four columns (case-sensitive):
- `roomNumber` - The room number/identifier (must be unique)
- `roomCapacity` - The maximum capacity of the room (must be a positive number)
- `roomFloor` - The floor where the room is located
- `roomBuilding` - The building where the room is located

### Exam Room CSV Format Example

```csv
roomNumber,roomCapacity,roomFloor,roomBuilding
Room 101,30,Ground Floor,Main Building
Room 102,25,Ground Floor,Main Building
Room 201,35,First Floor,Main Building
Lab A,20,Ground Floor,Science Building
Lab B,22,First Floor,Science Building
Auditorium A,100,Ground Floor,Auditorium Building
```

### Exam Room Upload Features
- **Duplicate Prevention**: Prevents duplicate room numbers
- **Capacity Validation**: Ensures room capacity is a positive number
- **Flexible Naming**: Supports various room naming conventions
- **Building Organization**: Organizes rooms by building and floor

## File Requirements

### General Requirements
- File must have a `.csv` extension
- First row must contain column headers
- File should be UTF-8 encoded
- Maximum file size: 10MB (configurable)

### Data Validation
- **Students**: Roll numbers must be unique within each class
- **Exam Rooms**: Room numbers must be globally unique
- **Capacity**: Must be positive integers for exam rooms
- **Required Fields**: Essential fields cannot be empty

## How to Use

### Via Web Interface

#### Student Upload
1. Go to the Class Management page
2. Click the "Upload CSV" button
3. Download the template (optional) to see the correct format
4. Select your CSV file
5. Click "Upload"
6. Review the upload results

#### Exam Room Upload
1. Go to the Exam Room Management page
2. Click the "Upload CSV" button
3. Download the template (optional) to see the correct format
4. Select your CSV file
5. Click "Upload"
6. Review the upload results

### Via API

#### Student Upload
```bash
curl -X POST "http://localhost:8000/upload-csv" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_students.csv"
```

#### Exam Room Upload
```bash
curl -X POST "http://localhost:8000/upload-exam-rooms-csv" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_exam_rooms.csv"
```

## Upload Results

### Student Upload Results
```json
{
  "message": "CSV upload completed",
  "summary": {
    "total_students_processed": 15,
    "classes_created": 3,
    "classes_updated": 1,
    "errors_count": 2
  },
  "details": {
    "created_classes": ["Computer Science A", "Mathematics B"],
    "updated_classes": ["Physics C"],
    "errors": [
      "Student CS101 already exists in class Computer Science A"
    ]
  }
}
```

### Exam Room Upload Results
```json
{
  "message": "Exam rooms CSV upload completed",
  "summary": {
    "total_rooms_processed": 10,
    "rooms_added": 8,
    "rooms_skipped": 2,
    "errors_count": 2
  },
  "details": {
    "errors": [
      "Room 101 already exists",
      "Invalid room capacity 'abc' in row 5"
    ]
  }
}
```

## Error Handling

### Common Errors and Solutions

#### Student Upload Errors
1. **"Missing required columns"**
   - Ensure CSV has: `className`, `rollNumber`, `studentName`
   - Check for typos in column names

2. **"Student already exists"**
   - This is a warning, not an error
   - The duplicate student will be skipped

#### Exam Room Upload Errors
1. **"Missing required columns"**
   - Ensure CSV has: `roomNumber`, `roomCapacity`, `roomFloor`, `roomBuilding`
   - Check for typos in column names

2. **"Invalid room capacity"**
   - Room capacity must be a positive number
   - Check for non-numeric values in capacity column

3. **"Room already exists"**
   - Room numbers must be unique
   - The duplicate room will be skipped

#### General Errors
1. **"File must be a CSV file"**
   - Ensure your file has a `.csv` extension
   - Don't use Excel files (.xlsx) - save as CSV instead

2. **"File encoding error"**
   - Save your CSV file with UTF-8 encoding
   - In Excel: File → Save As → CSV UTF-8

## Best Practices

### Data Preparation
1. **Clean your data** before uploading
   - Remove empty rows
   - Ensure consistent formatting
   - Check for typos in names

2. **Use consistent naming**
   - Keep class names consistent across uploads
   - Use a standard format for roll numbers and room numbers

3. **Test with small files first**
   - Upload a small sample to verify format
   - Check the results before uploading large files

### File Management
1. **Keep backups** of your original data
2. **Use descriptive filenames** (e.g., `students_fall_2024.csv`, `exam_rooms_main_building.csv`)
3. **Download templates** if you're unsure about the format

## Template Downloads

You can download properly formatted template files:

### Via Web Interface
- **Student Template**: Click "Download Template" in the student upload dialog
- **Exam Room Template**: Click "Download Template" in the exam room upload dialog

### Via API
- **Student Template**: `GET http://localhost:8000/download-csv-template`
- **Exam Room Template**: `GET http://localhost:8000/download-exam-rooms-csv-template`

## Troubleshooting

### Upload Fails Completely
1. Check file format and extension
2. Verify column names are correct
3. Ensure file is not corrupted
4. Try with a smaller file

### Partial Upload Success
1. Review the error messages in the upload results
2. Fix the problematic rows in your CSV
3. Re-upload the corrected file

### Data Not Appearing
1. Check if items were reported as duplicates
2. Verify names match exactly (case-sensitive)
3. Refresh the list in the UI

## Limitations

- Maximum file size: 10MB
- Maximum items per upload: 10,000
- Roll numbers must be unique within each class
- Room numbers must be globally unique
- Class names and room numbers are case-sensitive

## Support

If you encounter issues:
1. Check this guide first
2. Verify your CSV format matches the templates
3. Review the error messages in the upload results
4. Test with the provided sample files

## Sample Files

The repository includes sample CSV files:
- `sample_students.csv` - Example with multiple classes and students
- `sample_exam_rooms.csv` - Example with various room types and buildings
- Download templates from the application for the latest format
