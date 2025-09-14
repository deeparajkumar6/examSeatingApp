from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from ..models import ScheduleRequest, ScheduleResponse
from ..services import ScheduleService
from ..excel_export_service import ExcelExportService
from datetime import datetime

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.post("", response_model=ScheduleResponse)
def schedule_exam(data: ScheduleRequest):
    """Schedule exam seating arrangement"""
    return ScheduleService.schedule_exam(data)

@router.post("/export/excel/summary")
def export_summary_excel(data: dict):
    """Export seating arrangement summary as Excel"""
    excel_file = ExcelExportService.generate_summary_excel(data)
    
    filename = f"{data.get('title', 'Exam').replace(' ', '_')}_Summary_{data.get('date', datetime.now().strftime('%Y-%m-%d'))}.xlsx"
    
    return StreamingResponse(
        iter([excel_file.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.post("/export/excel/detailed")
def export_detailed_excel(data: dict):
    """Export detailed seating arrangement as Excel (one sheet per room)"""
    excel_file = ExcelExportService.generate_detailed_excel(data)

    filename = f"{data.get('title', 'Exam').replace(' ', '_')}_Detailed_{data.get('date', datetime.now().strftime('%Y-%m-%d'))}.xlsx"

    return StreamingResponse(
        iter([excel_file.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
