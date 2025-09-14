# Exam Seating Arrangement System

A comprehensive web application for managing exam seating arrangements with language-based student filtering, room capacity management, and PDF generation.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### 1. Start the Backend (FastAPI)

```bash
# Navigate to backend directory
cd fastapi_app

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Note: --reload flag enables auto-restart on code changes for development
```

The backend API will be available at: `http://localhost:8000`

### 2. Start the Frontend (Vue.js)

```bash
# Navigate to frontend directory (in a new terminal)
cd UI

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The frontend application will be available at: `http://localhost:3000`

### 3. Alternative: Start Both Apps with One Command

```bash
# From the root directory
python start_app.py
```

This will start both the backend and frontend servers automatically.

## 📋 Features

- **Student Management**: Import students from Excel/CSV files
- **Room Management**: Configure exam rooms with capacity
- **Language-Based Filtering**: Schedule exams based on student languages
- **Seating Arrangement**: Automatic seat allocation with room splitting
- **PDF Generation**: Generate seating charts and student lists
- **Real-time Validation**: Capacity analysis and conflict detection

## 🗂️ Project Structure

```
examSeatingApp/
├── fastapi_app/          # Backend API (FastAPI + SQLite)
│   ├── app/             # Application code
│   ├── database.db      # SQLite database
│   └── requirements.txt # Python dependencies
├── UI/                  # Frontend (Vue.js + Vuetify)
│   ├── src/            # Source code
│   ├── package.json    # Node.js dependencies
│   └── vite.config.mjs # Vite configuration
├── docs/               # Documentation
├── sample_*.csv        # Sample data files
└── start_app.py       # Unified app starter
```

## 🔧 Configuration

### Backend Configuration
- Database: SQLite (automatically created)
- Port: 8000 (configurable in uvicorn command)
- CORS: Enabled for frontend communication

### Frontend Configuration
- Port: 3000 (configurable in vite.config.mjs)
- API Base URL: http://localhost:8000
- Theme: Vuetify Material Design

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- **[Quick Start Guide](docs/QUICK_START.md)** - Detailed setup instructions
- **[CSV Upload Guide](docs/CSV_UPLOAD_GUIDE.md)** - Data import instructions
- **[Excel Import Guide](docs/UI_EXCEL_IMPORT_GUIDE.md)** - Excel file handling
- **[PDF Customization](docs/PDF_CUSTOMIZATION_GUIDE.md)** - PDF output customization
- **[API Documentation](docs/BULK_IMPORT_API.md)** - Backend API reference
- **[Language API](docs/LANGUAGE_API_EXAMPLE.md)** - Language filtering examples
- **[Theme Colors](docs/THEME_COLORS.md)** - UI customization
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## 🎯 Usage Workflow

1. **Setup Data**: Import students and exam rooms via CSV/Excel
2. **Create Schedule**: Select date, classes, and rooms
3. **Configure Options**: Set language filters and seating preferences
4. **Generate Arrangement**: Create optimized seating plan
5. **Export Results**: Download PDF reports and seating charts

## 🛠️ Development

### Backend Development
```bash
cd fastapi_app
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd UI
npm install
npm run dev
```

### Building for Production
```bash
# Frontend build
cd UI
npm run build

# Backend is ready for production as-is
```

## 📝 Sample Data

The project includes sample data files:
- `sample_students.csv` - Sample student data with languages
- `sample_exam_rooms.csv` - Sample room configurations
- `I YEAR STUDENT LIST.xlsx` - Excel format sample

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. Review the relevant documentation in the `docs/` folder
3. Check the browser console and server logs for errors

---

**Happy Scheduling! 🎓**
