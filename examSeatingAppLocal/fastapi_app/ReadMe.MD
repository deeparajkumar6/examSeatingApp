# Exam Seating App - Clean Modular FastAPI Application

## 🎯 Clean Project Structure

```
fastapi_app/
├── app/                     # Main application package
│   ├── __init__.py         # Package initialization
│   ├── main.py             # Application factory and setup
│   ├── config.py           # Configuration settings
│   ├── database.py         # Database connection and management
│   ├── models.py           # Pydantic data models
│   ├── services.py         # Business logic services
│   ├── csv_utils.py        # CSV processing utilities
│   └── routes/             # API endpoint routes
│       ├── __init__.py
│       ├── classes.py      # Class management endpoints
│       ├── students.py     # Student management endpoints
│       ├── exam_rooms.py   # Exam room management endpoints
│       ├── schedule.py     # Scheduling endpoints
│       └── csv_routes.py   # CSV upload/download endpoints
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── database.db            # SQLite database
└── README.md              # This documentation
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Access the API
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Base URL**: http://localhost:8000

## 📋 API Endpoints

### Classes Management
- `GET /class` - Get all classes with students
- `POST /class` - Create a new class with students
- `PUT /class/{class_id}` - Update an existing class
- `DELETE /class/{class_id}` - Delete a class and all its students

### Student Management
- `GET /student/{class_id}` - Get all students in a specific class
- `POST /student/{class_id}` - Add a new student to a class
- `DELETE /student/{student_id}` - Delete a student

### Exam Room Management
- `GET /examRoom` - Get all exam rooms
- `POST /examRoom` - Create a new exam room
- `PUT /examRoom/{room_id}` - Update an existing exam room
- `DELETE /examRoom/{room_id}` - Delete an exam room

### Exam Scheduling
- `POST /schedule` - Create exam seating arrangement

### CSV Operations
- `POST /upload-csv` - Upload student data via CSV
- `GET /download-csv-template` - Download student CSV template
- `POST /upload-exam-rooms-csv` - Upload exam rooms via CSV
- `GET /download-exam-rooms-csv-template` - Download exam rooms CSV template

## ⚙️ Configuration

Edit `app/config.py` to modify:
- Database file path
- CORS settings
- Maximum students per class per room
- API metadata

## 🗄️ Database

The application uses SQLite with the following tables:
- **classes**: Store class information
- **students**: Store student data linked to classes
- **examRooms**: Store exam room details

## 🎯 Key Features

- **Modular Architecture**: Clean separation of concerns
- **Type Safety**: Full type hints throughout
- **Error Handling**: Comprehensive error management
- **CSV Support**: Bulk upload/download functionality
- **Flexible Scheduling**: Smart student distribution across rooms
- **CORS Enabled**: Ready for frontend integration

## 🔧 Development

### Adding New Features
1. **New API endpoints**: Add routes in `app/routes/`
2. **Business logic**: Extend services in `app/services.py`
3. **Data models**: Add models in `app/models.py`
4. **Database changes**: Update `app/database.py`

### Testing
The application includes comprehensive error handling and validation. Test all endpoints using the interactive documentation at `/docs`.

## 📦 Dependencies

- **FastAPI**: Modern web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Python-multipart**: File upload support

## 🎉 Benefits

- **Clean Code**: Well-organized and maintainable
- **Scalable**: Easy to extend and modify
- **Professional**: Follows industry best practices
- **Documented**: Comprehensive API documentation
- **Tested**: Verified functionality
