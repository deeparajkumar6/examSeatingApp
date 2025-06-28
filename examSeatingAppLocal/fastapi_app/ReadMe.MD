# Exam Seating App API

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Activate virtual environment (if using):
```bash
# Windows
.\.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. Run database migration (if upgrading from old version):
```bash
python migrate_database.py
```

4. Start the API server:
```bash
fastapi dev main.py
```

The API will be available at `http://localhost:8000`

## New Features

### CSV Upload Functionality
- **Bulk Import**: Upload students from CSV files
- **Template Download**: Get a properly formatted CSV template
- **Error Handling**: Detailed feedback on upload results
- **Class Management**: Automatically creates new classes or updates existing ones

### CSV Format Requirements
The CSV file must contain these columns:
- `className` - Name of the class
- `rollNumber` - Student's roll number (can be non-sequential)
- `studentName` - Student's name (optional, can be empty)

Example CSV:
```csv
className,rollNumber,studentName
Computer Science A,CS101,Alice Johnson
Computer Science A,CS103,Bob Smith
Mathematics B,MATH201,Eve Wilson
Mathematics B,MATH203,Frank Miller
```

## Changes in New Version

- **Explicit Student Management**: Instead of roll number ranges, you can now add individual students with specific roll numbers
- **Missing Roll Numbers**: Supports scenarios where some roll numbers might be missing from a sequence
- **Student Names**: Optional student names can be added alongside roll numbers
- **Bulk Import**: UI supports bulk adding of students via text input
- **CSV Upload**: Upload students from CSV files with automatic class creation
- **Better Scheduling**: Improved seating arrangement algorithm that works with explicit student lists

## API Endpoints

### Class Management
- `GET /class` - Get all classes with their students
- `POST /class` - Create a new class with students
- `PUT /class/{id}` - Update a class and its students
- `DELETE /class/{id}` - Delete a class and all its students

### Student Management
- `GET /student/{class_id}` - Get students for a specific class
- `POST /student/{class_id}` - Add a student to a class
- `DELETE /student/{id}` - Delete a student

### CSV Upload
- `POST /upload-csv` - Upload students from CSV file
- `GET /download-csv-template` - Download CSV template for students
- `POST /upload-exam-rooms-csv` - Upload exam rooms from CSV file
- `GET /download-exam-rooms-csv-template` - Download CSV template for exam rooms

### Exam Room Management
- `GET /examRoom` - Get all exam rooms
- `POST /examRoom` - Create a new exam room
- `PUT /examRoom/{id}` - Update an exam room
- `DELETE /examRoom/{id}` - Delete an exam room

### Scheduling
- `POST /schedule` - Generate seating arrangement

## Testing

Run the test scripts to verify functionality:
```bash
# Test basic API functionality
python test_api.py

# Test CSV upload functionality
python test_csv_upload.py
```
