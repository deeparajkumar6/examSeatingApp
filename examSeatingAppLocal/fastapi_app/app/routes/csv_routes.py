from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from ..csv_utils import CSVProcessor, CSVTemplates

router = APIRouter(tags=["csv"])

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload CSV file with columns: className, rollNumber, studentName
    Creates classes and students from the CSV data
    """
    return await CSVProcessor.process_students_csv(file)

@router.get("/download-csv-template")
def download_csv_template():
    """Download a CSV template file for bulk student upload"""
    template_content = CSVTemplates.get_student_template()
    
    return Response(
        content=template_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=student_upload_template.csv"}
    )

@router.post("/upload-exam-rooms-csv")
async def upload_exam_rooms_csv(file: UploadFile = File(...)):
    """
    Upload CSV file with columns: roomNumber, roomCapacity, roomFloor, roomBuilding
    Creates exam rooms from the CSV data
    """
    return await CSVProcessor.process_exam_rooms_csv(file)

@router.get("/download-exam-rooms-csv-template")
def download_exam_rooms_csv_template():
    """Download a CSV template file for bulk exam room upload"""
    template_content = CSVTemplates.get_exam_room_template()
    
    return Response(
        content=template_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=exam_rooms_upload_template.csv"}
    )
