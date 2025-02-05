import uuid
from datetime import datetime


from interview_scheduler.core.config.constants import PostgreSqlInfo
from interview_scheduler.core.logging.logger import logger
from interview_scheduler.core.utils.RDBMS_utils import RDBMSUtility


def create_token(user_id, expire_time,):
    """
    This method is to create a cookie
    """
    try:
        uid = str(uuid.uuid4()).replace("-", "")
        created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_exists_query = f"""select * from {PostgreSqlInfo.session_table} where user_id = '{user_id}'"""
        status, session_exists = RDBMSUtility().execute_select_query_fetch_one(session_exists_query)
        if status and session_exists is not None and len(session_exists) > 0:
            logger.info("User session already exist")
            session_update_query = f"""UPDATE {PostgreSqlInfo.session_table} SET created_time = '{created_time}',
                    session_expire = '{expire_time}',uid = '{uid}'
                    where user_id = '{user_id}'"""
            status, add_session = RDBMSUtility().update_postgress_table_data(session_update_query)
            if status:
                logger.info("Successfully updated the session")
            else:
                raise Exception("Failed to update the session")
        else:
            add_session_query = f"""Insert into {PostgreSqlInfo.session_table}(uid,user_id,created_time,
                        session_expire) Values('{uid}','{user_id}','{created_time}',
                        '{expire_time}')"""
            status, add_session = RDBMSUtility().insert_postgress_table(add_session_query)
            if status:
                logger.info("Successfully recorded the session")
            else:
                raise Exception("Failed to record the session")
        return user_id, uid
    except Exception:
        raise
