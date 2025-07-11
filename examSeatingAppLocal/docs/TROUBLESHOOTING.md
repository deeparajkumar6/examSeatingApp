# Troubleshooting Guide

## Common Issues and Solutions

### 1. 404 Error: Bulk Import Endpoints Not Found

**Error Message:**
```
POST http://localhost:8000/bulk-import/validate 404 (Not Found)
```

**Cause:** FastAPI server is not running or not properly configured.

**Solutions:**

#### Option A: Start Server with Startup Script
```bash
cd /path/to/examSeatingApp/examSeatingAppLocal
python3 start_fastapi.py
```

#### Option B: Start Server Manually
```bash
cd /path/to/examSeatingApp/examSeatingAppLocal/fastapi_app
python3 main.py
```

#### Option C: Using uvicorn directly
```bash
cd /path/to/examSeatingApp/examSeatingAppLocal/fastapi_app
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Server Health Check

**Test if server is running:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

### 3. Test Bulk Import Endpoints

**Test template endpoint:**
```bash
curl http://localhost:8000/bulk-import/template
```

**Test validation endpoint:**
```bash
curl -X POST -F "file=@your_excel_file.xlsx" http://localhost:8000/bulk-import/validate
```

### 4. Database Issues

**Error:** Database connection or table creation issues

**Solution:** Ensure database is properly initialized:
```bash
cd /path/to/examSeatingApp/examSeatingAppLocal/fastapi_app
python3 -c "from app.database import init_database; init_database(); print('Database initialized')"
```

### 5. Missing Dependencies

**Error:** Import errors or missing modules

**Solution:** Install required dependencies:
```bash
cd /path/to/examSeatingApp/examSeatingAppLocal/fastapi_app
pip install -r requirements.txt
```

### 6. CORS Issues

**Error:** Cross-origin request blocked

**Solution:** Ensure CORS is properly configured in `app/config.py`:
```python
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173", "*"]
```

### 7. File Upload Issues

**Error:** File upload fails or validation errors

**Checklist:**
- [ ] File is .xlsx or .xls format
- [ ] File follows the required structure
- [ ] File size is reasonable (< 10MB)
- [ ] Server has write permissions

### 8. UI Development Server

**For Vue.js UI development:**
```bash
cd /path/to/examSeatingApp/examSeatingAppLocal/UI
npm run dev
```

**Default URL:** http://localhost:5173

## Development Workflow

### 1. Start Both Servers

**Terminal 1 - FastAPI Backend:**
```bash
cd examSeatingAppLocal
python3 start_fastapi.py
```

**Terminal 2 - Vue.js Frontend:**
```bash
cd examSeatingAppLocal/UI
npm run dev
```

### 2. Access Applications

- **Frontend UI:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### 3. Test Excel Import

1. Navigate to Classes page in UI
2. Click "Import from Excel"
3. Upload sample file: `I YEAR STUDENT LIST.xlsx`
4. Validate and import

## Debugging Steps

### 1. Check Server Logs

Look for error messages in the terminal where you started the FastAPI server.

### 2. Browser Developer Tools

1. Open browser developer tools (F12)
2. Check Console tab for JavaScript errors
3. Check Network tab for API request/response details

### 3. API Testing

Use tools like:
- **curl** (command line)
- **Postman** (GUI)
- **FastAPI docs** (http://localhost:8000/docs)

### 4. Database Inspection

**Check database contents:**
```bash
cd examSeatingAppLocal/fastapi_app
sqlite3 database.db
.tables
SELECT * FROM classes;
SELECT * FROM students;
.quit
```

## Environment Setup

### Required Software

1. **Python 3.8+**
2. **Node.js 16+**
3. **npm or yarn**

### Python Dependencies

```bash
pip install fastapi uvicorn pandas openpyxl python-multipart
```

### Node.js Dependencies

```bash
cd UI
npm install
```

## Configuration Files

### FastAPI Configuration
- `fastapi_app/app/config.py` - Server configuration
- `fastapi_app/requirements.txt` - Python dependencies

### Vue.js Configuration
- `UI/package.json` - Node.js dependencies
- `UI/vite.config.mjs` - Build configuration

## Getting Help

### Log Files
- FastAPI logs: Check terminal output
- Vue.js logs: Check browser console
- Database logs: Check SQLite error messages

### Common Error Patterns

1. **Import Errors:** Missing Python packages
2. **404 Errors:** Server not running or wrong URL
3. **CORS Errors:** Frontend/backend URL mismatch
4. **File Errors:** Wrong Excel format or permissions

### Support Resources

1. **FastAPI Documentation:** https://fastapi.tiangolo.com/
2. **Vue.js Documentation:** https://vuejs.org/
3. **Vuetify Documentation:** https://vuetifyjs.com/

## Quick Fix Commands

**Restart everything:**
```bash
# Kill any running servers
pkill -f "python.*main.py"
pkill -f "node.*vite"

# Start FastAPI
cd examSeatingAppLocal
python3 start_fastapi.py &

# Start Vue.js (in new terminal)
cd examSeatingAppLocal/UI
npm run dev
```

**Reset database:**
```bash
cd examSeatingAppLocal/fastapi_app
rm -f database.db
python3 -c "from app.database import init_database; init_database()"
```

**Clear browser cache:**
- Press Ctrl+Shift+R (hard refresh)
- Or clear browser cache manually
