class PostgreSqlInfo:
    roles_table = "roles"
    user_table = "users"
    session_table = "sessions"
    schedule_table = "schedule"


class ServiceDetails:
    service_host = "0.0.0.0"
    service_port = 8420


class PostgreSqlCreds:
    host = "localhost"
    port = 5432
    user = "postgres"
    password = "test@123"
    database = "postgres"


class Secrets:
    LOCK_OUT_TIME_MINS = 60
    leeway_in_mins = 10
    token_name = 'ZS-BrainCase'
    issuer = "BrainCase"
    session_id = "user_id"
    alg = "RS256"


class ResponseMessage:
    @staticmethod
    def final_json(status, message, data=dict(), meta=None):
        if meta is None:
            json = {"status": status, "message": message, "data": data}
        else:
            json = {"status": status, "message": message, "data": data, "meta_data": meta}

        return json


class Message:
    success = "success"
    failure = "failure"
