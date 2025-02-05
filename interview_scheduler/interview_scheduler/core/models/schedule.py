from pydantic import BaseModel


class Schedule(BaseModel):
    user_id: int
    start_time: int
    end_time: int


class TimeSlots(BaseModel):
    candidate_id: int
    interviewer_id: int
