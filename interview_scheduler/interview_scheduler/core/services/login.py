from fastapi import APIRouter, Request, Response
from interview_scheduler.core.handlers.login_handler import LoginHandler
from interview_scheduler.core.logging.logger import logger
from interview_scheduler.core.models.login import LoginInput, LogoutInput
from interview_scheduler.core.utils.login_util import create_token

router = APIRouter()


@router.post("/login", tags=["login"])
def login(req_json: LoginInput, response: Response, request: Request):
    try:
        result = LoginHandler().login_access(req_json=req_json)
        if result["status"] != "failure":
            session_id, login_token = create_token(user_id=result["data"]["user_list"]["user_id"],
                                                   expire_time=result["data"]["user_list"]["expire_time"])
            response.set_cookie(key="auth_token", value=login_token, httponly=True, samesite='strict', max_age=2592000)
        return {"status": result["status"], "message": result["message"], "data": result["data"]}

    except Exception as e:
        logger.error("Exception occurred while logging in -> " + str(e))
        return {"status": "failure", "message": "Error occurred while logging in"}


@router.post("/logout", tags=["login"])
def logout(req_json: LogoutInput):
    try:
        result = LoginHandler.remove_session(req_json)
        return result

    except Exception as e:
        logger.error("Exception occurred while logging out -> " + str(e))
        return {"status": "failure", "message": "Error occurred while logging out"}
