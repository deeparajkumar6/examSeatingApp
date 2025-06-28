# Quick Start Guide

## 🚀 Getting Started

### 1. Start the Application
```bash
# Terminal 1 - Start API
cd fastapi_app
pip install -r requirements.txt
fastapi dev main.py

# Terminal 2 - Start UI
cd UI
npm install
npm run dev
```

### 2. Access the Application
- **API**: http://localhost:8000
- **UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## 📊 Adding Data

### Option 1: Manual Entry
1. **Classes**: Go to Class Management → Add Class → Add students individually
2. **Exam Rooms**: Go to Exam Room Management → Add Exam Room

### Option 2: CSV Upload (Recommended for Bulk Data)

#### Students CSV Upload
1. Go to **Class Management**
2. Click **"Upload CSV"**
3. Download template or use this format:
```csv
className,rollNumber,studentName
Computer Science A,CS101,Alice Johnson
Computer Science A,CS103,Bob Smith
Mathematics B,MATH201,Eve Wilson
```

#### Exam Rooms CSV Upload
1. Go to **Exam Room Management**
2. Click **"Upload CSV"**
3. Download template or use this format:
```csv
roomNumber,roomCapacity,roomFloor,roomBuilding
Room 101,30,Ground Floor,Main Building
Room 102,25,Ground Floor,Main Building
Lab A,20,Ground Floor,Science Building
```

## 📅 Generating Schedules

1. Go to **Schedule** page
2. Select **exam date**
3. Choose **classes** to include
4. Choose **exam rooms** to use
5. Toggle **"Split Students"** if you want to distribute students across multiple rooms
6. Click **"Generate Schedule"**
7. **Export to PDF** if needed

## 💡 Tips

### For Students
- ✅ Roll numbers can be non-sequential (101, 103, 105 is fine)
- ✅ Student names are optional
- ✅ Same class name will add to existing class
- ❌ Duplicate roll numbers in same class will be skipped

### For Exam Rooms
- ✅ Room numbers must be unique
- ✅ Capacity must be a positive number
- ✅ Floor and building help organize rooms
- ❌ Duplicate room numbers will be skipped

### For Scheduling
- 📊 Total room capacity must be ≥ total students
- 🔄 "Split Students" distributes students across rooms
- 📄 Export schedules as PDF for printing with college branding
- 🎯 Algorithm tries to limit students from same class per room
- 🏫 PDF includes college logo, name, and page numbers
- 🎨 Professional burgundy and navy color scheme

## 📁 Sample Files

The repository includes sample files:
- `sample_students.csv` - Example student data
- `sample_exam_rooms.csv` - Example room data

## 🆘 Troubleshooting

### CSV Upload Issues
1. **File format**: Must be `.csv` (not Excel)
2. **Encoding**: Save as UTF-8
3. **Headers**: First row must have exact column names
4. **Data**: Check for empty required fields

### Common Errors
- **"Missing required columns"**: Check column names spelling
- **"Invalid room capacity"**: Must be a positive number
- **"Student already exists"**: Duplicate roll numbers are skipped
- **"Not enough capacity"**: Add more rooms or reduce students

### Getting Help
1. Check `CSV_UPLOAD_GUIDE.md` for detailed instructions
2. Use template downloads for correct format
3. Test with small files first
4. Check error messages in upload results

## 🎯 Workflow Example

1. **Prepare Data**
   - Create students CSV with all classes
   - Create exam rooms CSV with all available rooms

2. **Upload Data**
   - Upload students CSV → Creates classes automatically
   - Upload exam rooms CSV → Sets up all rooms

3. **Generate Schedule**
   - Select date and classes for the exam
   - Choose appropriate rooms
   - Generate and export schedule

4. **Ready for Exam!**
   - Print PDF schedules
   - Post room assignments
   - Conduct exam with organized seating

---

**Need more help?** Check the full documentation in `CSV_UPLOAD_GUIDE.md`
