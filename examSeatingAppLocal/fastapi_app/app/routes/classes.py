from fastapi import APIRouter
from typing import Dict
from ..models import ClassModel, ClassResponseModel
from ..services import ClassService

router = APIRouter(prefix="/class", tags=["classes"])

@router.get("", response_model=Dict)
def get_classes():
    """Get all classes with their students"""
    classes = ClassService.get_all_classes()
    return {"classes": classes}

@router.post("")
def add_class(class_data: ClassModel):
    """Add a new class with students"""
    ClassService.create_class(class_data)
    return {"message": "Class added successfully"}

@router.put("/{class_id}")
def update_class(class_id: int, class_data: ClassModel):
    """Update an existing class"""
    ClassService.update_class(class_id, class_data)
    return {"message": "Class updated successfully"}

@router.delete("/{class_id}")
def delete_class(class_id: int):
    """Delete a class and all its students"""
    ClassService.delete_class(class_id)
    return {"message": "Class deleted successfully"}

@router.get("/download/sample-template")
def download_sample_template():
    """Download sample Excel template for class data import"""
    from ..sample_template_service import SampleTemplateService
    from datetime import datetime
    from fastapi.responses import StreamingResponse
    
    template_file = SampleTemplateService.generate_sample_template()
    
    filename = f"Class_Import_Template_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    return StreamingResponse(
        iter([template_file.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
