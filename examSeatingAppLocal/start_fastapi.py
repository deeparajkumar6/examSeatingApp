#!/usr/bin/env python3
"""
FastAPI Server Startup Script
"""
import uvicorn
import sys
import os

# Add the fastapi_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fastapi_app'))

from app.main import app

if __name__ == "__main__":
    print("Starting FastAPI server...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
