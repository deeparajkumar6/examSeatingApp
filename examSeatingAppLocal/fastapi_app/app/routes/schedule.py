from fastapi import APIRouter
from ..models import ScheduleRequest, ScheduleResponse
from ..services import ScheduleService

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.post("", response_model=ScheduleResponse)
def schedule_exam(data: ScheduleRequest):
    """Schedule exam seating arrangement"""
    return ScheduleService.schedule_exam(data)
