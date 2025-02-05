from datetime import (
    datetime,
    timedelta,
)
from interview_scheduler.core.config.constants import (
    PostgreSqlInfo,
    ResponseMessage,
    Message,
)
from interview_scheduler.core.logging.logger import logger
from interview_scheduler.core.utils.RDBMS_utils import RDBMSUtility


class ScheduleHandler:
    @staticmethod
    def schedule_time_slot(req_json):
        try:
            start_time = req_json.get("start_time", 0)
            end_time = req_json.get("end_time", 0)
            user_id = req_json.get("user_id", "")

            insert_query = f"""
                        INSERT INTO {PostgreSqlInfo.schedule_table} (user_id, start_time, end_time)
                        VALUES (%s, %s, %s)
                    """
            params = (user_id, start_time, end_time)
            status, result = RDBMSUtility().insert_postgress_table(insert_query, params)

            if status:
                logger.info("Time slot registered successfully")
                return ResponseMessage.final_json(
                    Message.success, "Time slot registered successfully"
                )
            else:
                return ResponseMessage.final_json(
                    Message.failure, "Failed to register time slot"
                )

        except Exception as e:
            return {"status": "failure", "message": str(e)}

    @staticmethod
    def get_available_slots(user_id: str):
        """Fetch available time slots for a user (candidate/interviewer) from the database."""
        query = f"""
                SELECT start_time, end_time
                FROM schedule
                WHERE user_id = {user_id}
                """
        status, result = RDBMSUtility().execute_select_query(query)
        if status and result:
            return [(res.get("start_time"), res.get("end_time")) for res in result]
        return []

    @staticmethod
    def find_common_slots(candidate_slots, interviewer_slots):
        """Calculate the common available time slots between candidate and interviewer."""
        try:
            intersecting_slots = []

            for candidate_start, candidate_end in candidate_slots:
                for interviewer_start, interviewer_end in interviewer_slots:
                    candidate_start = f"{candidate_start:02d}:00"
                    candidate_end = f"{candidate_end:02d}:00"
                    interviewer_start = f"{interviewer_start:02d}:00"
                    interviewer_end = f"{interviewer_end:02d}:00"

                    candidate_start_dt = datetime.strptime(
                        f"2025-02-05 {candidate_start}", "%Y-%m-%d %H:%M"
                    )
                    candidate_end_dt = datetime.strptime(
                        f"2025-02-05 {candidate_end}", "%Y-%m-%d %H:%M"
                    )
                    interviewer_start_dt = datetime.strptime(
                        f"2025-02-05 {interviewer_start}", "%Y-%m-%d %H:%M"
                    )
                    interviewer_end_dt = datetime.strptime(
                        f"2025-02-05 {interviewer_end}", "%Y-%m-%d %H:%M"
                    )

                    overlap_start = max(
                        candidate_start_dt,
                        interviewer_start_dt,
                    )
                    overlap_end = min(
                        candidate_end_dt,
                        interviewer_end_dt,
                    )

                    current_time = overlap_start
                    while current_time + timedelta(hours=1) <= overlap_end:
                        next_time = current_time + timedelta(hours=1)
                        intersecting_slots.append(
                            (
                                current_time.hour,
                                next_time.hour,
                            )
                        )
                        current_time = next_time

            return ResponseMessage.final_json(Message.success, intersecting_slots)
        except Exception as e:
            return {"status": "failure", "message": str(e)}
