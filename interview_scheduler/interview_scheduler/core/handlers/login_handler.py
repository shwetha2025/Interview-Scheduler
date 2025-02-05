from datetime import (
    datetime,
    timedelta,
)
from interview_scheduler.core.config.constants import (
    Secrets,
    PostgreSqlInfo,
    ResponseMessage,
    Message,
)
from interview_scheduler.core.logging.logger import logger
from interview_scheduler.core.utils.RDBMS_utils import RDBMSUtility


class LoginHandler:
    def login_access(self, req_json, cognito_data=None):
        try:
            logger.info("Inside login access")
            user_access = self.access_verification(dict(req_json), cognito_data)

            if user_access["status"]:
                expire_time = datetime.today() + timedelta(
                    minutes=Secrets.LOCK_OUT_TIME_MINS
                )

                data = {
                    "user_list": {
                        "user_id": user_access["user_details"]["id"],
                        "name": user_access["user_details"]["name"],
                        "role_id": user_access["user_details"]["role_id"],
                        "expire_time": expire_time,
                    }
                }

                dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                update_user_details_query = f"""UPDATE {PostgreSqlInfo.user_table} SET
                       last_login = '{dt_string}'
                       WHERE id = {user_access["user_details"]["id"]}"""
                u_status, update_user_details_query_result = (
                    RDBMSUtility().update_postgress_table_data(
                        update_user_details_query
                    )
                )

                if u_status:
                    logger.debug("Successfully inserted the last login time")
                    return ResponseMessage.final_json(
                        Message.success,
                        f"Successfully logged in {user_access['user_details']['name']}",
                        data,
                    )
                else:
                    logger.info("Failed to insert last login time")
                    return ResponseMessage.final_json(
                        Message.failure,
                        f"Failed to login {user_access['user_details']['name']}",
                        data,
                    )

            else:
                return ResponseMessage.final_json(
                    Message.failure, user_access["message"]
                )
        except Exception as e:
            logger.error(f"Exception occurred while logging in: {str(e)}")
            raise Exception("Failed to login:" + str(e))

    def access_verification(self, req_json, cognito_data=None):
        try:
            logger.info("Inside access verification")
            username = req_json.get("username", "")
            password = req_json.get("password", "")

            if not username or not password:
                return {"message": "Username or password is missing.", "status": False}
            if cognito_data:
                pass
            else:
                query = f"""
                        SELECT u.password, u.id, u.name, u.role_id
                        FROM users u
                        JOIN roles r ON r.id = u.role_id
                        WHERE u.name = '{username}'
                    """
                status, access = RDBMSUtility().execute_select_query(query)

                if status and access:
                    # TODO: Can add hashed password for more security
                    stored_hashed_password = access[0]["password"]
                    if stored_hashed_password == password:
                        logger.debug(f"User verified for username: {username}")
                        return {
                            "message": "User verified",
                            "user_details": access[0],
                            "status": True,
                        }
                    else:
                        logger.debug(
                            f"Unauthorized/Invalid credentials for username: {username}"
                        )
                        return {
                            "message": "Unauthorized/Invalid credentials",
                            "status": False,
                        }
                else:
                    logger.debug(
                        f"Unauthorized/Invalid credentials for username: {username}"
                    )
                    return {
                        "message": "Unauthorized/Invalid credentials",
                        "status": False,
                    }
        except Exception as e:
            logger.error(f"Exception occurred while verifying credentials: {str(e)}")
            raise Exception("Failed to validate username and password:" + str(e))

    @staticmethod
    def remove_session(req_json):
        try:
            logger.info("Inside remove_session")

            session_exists_query = f"""SELECT * FROM {PostgreSqlInfo.session_table} 
                                        WHERE user_id = {req_json["user_id"]}"""
            status, session_exists = RDBMSUtility().execute_select_query_fetch_one(
                session_exists_query
            )
            if status and session_exists:
                logger.debug("User session exists")
                session_delete_query = f"""DELETE FROM {PostgreSqlInfo.session_table} 
                                            WHERE user_id = {req_json["user_id"]}"""
                status, delete_session = RDBMSUtility().delete_postgress_table_records(
                    session_delete_query
                )
                if status:
                    logger.info("Successfully deleted the session")
                    return ResponseMessage.final_json(
                        Message.success, "Logged out successfully"
                    )
                else:
                    raise Exception("Failed to delete the session")
            else:
                raise Exception("Failed to Logout: User not present")

        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            raise Exception("Failed to Logout: " + str(e))
