from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from typing import Dict
from ..models import BulkImportResponse
from ..services import ClassService

router = APIRouter(prefix="/bulk-import", tags=["bulk-import"])

@router.post("/excel", response_model=BulkImportResponse)
async def bulk_import_excel(file: UploadFile = File(...)):
    """
    Bulk import classes and students from Excel file
    
    Expected Excel format:
    - Academic year information in early rows
    - Header row with: S.No, Register Number, Names with Date of Birth, Dept/Class, Shift, Language
    - Student data split across two rows:
      * Row 1: Serial No, Register No, Name, Department, Shift, Language
      * Row 2: Date of Birth (in the Names with Date of Birth column)
    """
    
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload an Excel file (.xlsx or .xls)"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Process the Excel file
        result = ClassService.bulk_import_from_excel(file_content, file.filename)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/template")
async def download_template():
    """
    Download Excel template for bulk import
    """
    return JSONResponse(content={
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
            ],
            "example": {
                "headers": ["S.No", "Register Number", "Names with Date of Birth", "Dept / Class", "Shift", "Language"],
                "student_row_1": [1, 122302982, "John Doe", "I B.COM -CS", "I", "ENGLISH"],
                "dob_row_1": ["", "", "2000-06-22", "", "", ""],
                "student_row_2": [2, 122302983, "Jane Smith", "I B.COM -CS", "I", "HINDI"],
                "dob_row_2": ["", "", "2001-03-15", "", "", ""]
            }
        },
        "notes": [
            "Shift is mapped to the class (e.g., 'I' for first shift)",
            "Language is optional and mapped to individual students",
            "Date of birth should be in YYYY-MM-DD format or Excel date format",
            "Register numbers must be unique within each class",
            "If a class already exists, students will be updated"
        ]
    })

@router.post("/validate")
async def validate_excel(file: UploadFile = File(...)):
    """
    Validate Excel file without importing data
    """
    
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload an Excel file (.xlsx or .xls)"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Parse Excel file (without importing)
        from ..excel_utils import ExcelParser, ExcelValidator
        
        parsed_data = ExcelParser.parse_student_excel(file_content, file.filename)
        validation_errors = ExcelValidator.validate_parsed_data(parsed_data)
        
        # Prepare summary
        total_students = sum(len(class_data['students']) for class_data in parsed_data['classes'])
        
        response = {
            "valid": len(validation_errors) == 0,
            "errors": validation_errors,
            "summary": {
                "academic_year": parsed_data.get('academic_year'),
                "total_classes": len(parsed_data['classes']),
                "total_students": total_students,
                "classes": [
                    {
                        "class_name": class_data['class_name'],
                        "shift": class_data['shift'],
                        "student_count": len(class_data['students'])
                    }
                    for class_data in parsed_data['classes']
                ]
            }
        }
        
        return JSONResponse(content=response)
        
    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "valid": False,
                "errors": [f"Error parsing file: {str(e)}"],
                "summary": None
            }
        )

@router.post("/excel/selective", response_model=BulkImportResponse)
async def selective_import_excel(
    file: UploadFile = File(...),
    selected_classes: str = Form(...)
):
    """
    Import only selected classes from Excel file
    
    Args:
        file: Excel file to import
        selected_classes: JSON string of selected class objects (e.g., '[{"class_name":"I B.COM -CS","shift":"I"}]')
    """
    
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload an Excel file (.xlsx or .xls)"
        )
    
    try:
        import json
        
        # Parse selected class identifiers
        selected_class_identifiers = json.loads(selected_classes)
        
        # Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Process the Excel file with selective import
        result = ClassService.selective_import_from_excel(file_content, selected_class_identifiers, file.filename)
        
        return result
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid selected_classes format")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
