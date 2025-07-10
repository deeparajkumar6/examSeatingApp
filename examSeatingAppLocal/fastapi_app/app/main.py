from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_database
from .routes import classes, students, exam_rooms, schedule, csv_routes
from .config import settings

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION
    )

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS, 
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Initialize database
    init_database()

    # Include routers
    app.include_router(classes.router)
    app.include_router(students.router)
    app.include_router(exam_rooms.router)
    app.include_router(schedule.router)
    app.include_router(csv_routes.router)

    @app.get("/")
    def root():
        return {"message": "Exam Seating App API is running"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    return app

app = create_app()
