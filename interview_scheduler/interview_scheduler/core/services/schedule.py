from fastapi import (
    APIRouter,
    Request,
    Response,
)

from interview_scheduler.core.config.constants import (
    ResponseMessage,
    Message,
)
from interview_scheduler.core.logging.logger import logger
from interview_scheduler.core.models.schedule import (
    Schedule,
    TimeSlots,
)
from interview_scheduler.core.handlers.schedule_handler import ScheduleHandler

sched_router = APIRouter()


@sched_router.post("/register", tags=["scheduling"])
def register(req_json: Schedule, response: Response, request: Request):
    try:
        result = ScheduleHandler().schedule_time_slot(req_json=req_json.dict())
        if result["status"] != "failure":
            return {
                "status": result["status"],
                "message": result["message"],
                "data": result["data"],
            }
        else:
            return {
                "status": result["status"],
                "message": result["message"],
                "data": result["data"],
            }
    except Exception as e:
        logger.error("Exception occurred while logging in: " + str(e))
        return ResponseMessage.final_json(
            Message.failure, "Error occurred while registering"
        )


@sched_router.post("/get_schedulable_time_slots", tags=["scheduling"])
def get_schedulable_time_slots(request: TimeSlots):
    req_json = request.dict()
    candidate_id = req_json.get("candidate_id", "")
    interviewer_id = req_json.get("interviewer_id", "")

    candidate_slots = ScheduleHandler().get_available_slots(candidate_id)
    interviewer_slots = ScheduleHandler().get_available_slots(interviewer_id)

    schedulable_slots = ScheduleHandler().find_common_slots(
        candidate_slots, interviewer_slots
    )

    return schedulable_slots
