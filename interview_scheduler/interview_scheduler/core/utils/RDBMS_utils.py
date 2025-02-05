import psycopg2

from interview_scheduler.core.config.constants import PostgreSqlCreds
from interview_scheduler.core.logging.logger import logger


class RDBMSUtility(object):
    def __init__(self):
        """
            Initializer
        """
        try:
            self.db = psycopg2.connect(dbname=PostgreSqlCreds.database,
                                       user=PostgreSqlCreds.user,
                                       password=PostgreSqlCreds.password,
                                       host=PostgreSqlCreds.host,
                                       port=int(PostgreSqlCreds.port), )

        except Exception as e:
            raise Exception("Exception while establishing connection to database")

    def execute_select_query(self, qry):
        """
            This function is to execute select query
            :param :
            :return:
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(qry)
            columns = list(cursor.description)
            result = cursor.fetchall()
            results = []
            for row in result:
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col.name] = row[i]
                results.append(row_dict)
            cursor.close()
            return True, results

        except Exception as e:
            logger.exception("Error executing select query - {}".format(str(e)))
            return False, str(e)

    def execute_select_query_fetch_one(self, qry):
        """
            This function is to execute select query fetching one details
            :param :
            :return:
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(qry)
            columns = list(cursor.description)
            result = cursor.fetchone()
            row_dict = {}
            for i, col in enumerate(columns):
                if result:
                    row_dict[col.name] = result[i]
            cursor.close()
            return True, row_dict
        except Exception as e:
            logger.exception("Error executing select query - {}".format(str(e)))
            return False, str(e)

    def execute_query(self, qry, required):
        """
            This function is to execute a given query
            :param :
            :return:
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(qry)
            rows = None
            self.db.commit()
            if required:
                columns = list(cursor.description)
                result = cursor.fetchall()
                results = []
                for row in result:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        row_dict[col.name] = row[i]
                    results.append(row_dict)
                cursor.close()
                return True, results

            else:
                cursor.close()
        except Exception as e:
            logger.exception("Error executing query - {}".format(str(e)))
            return False, str(e)

    def insert_postgress_table(self, query, params):
        """
        This method is used for inserting new records in tables.

        :param query: The insert query to be executed
               params: parameters in the query
        :return: status: The status True on success and False on failure
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(query, params)
            self.db.commit()
            cursor.close()
            return True, "Success"
        except Exception as e:
            logger.error("Exception while updating: ", str(e))
            return False, str(e)

    def update_postgress_table_data(self, query):
        """
        This method is used for updating tables.

        :param query: The update query to be executed
        :return: status: The status True on success and False on failure
        """
        connection = None
        try:
            connection = self.db
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
            connection.close()
            return True, "Success"
        except Exception as e:
            logger.error("Exception while updating: ", str(e))
            return False, str(e)
        finally:
            try:
                if connection is not None:
                    logger.info("Connection closed")
            except Exception as e:
                logger.error("Exception while closing connection: ", str(e))
                return False, str(e)

    def delete_postgress_table_records(self, query):
        """
        This method is used for deleting table records.

        :param query: The update query to be executed
        :return: status: The status True on success and False on failure
        """
        connection = None
        try:
            connection = self.db
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
            connection.close()
            return True, "Success"
        except Exception as e:
            logger.error("Exception while updating: ", str(e))
            return False, str(e)
        finally:
            try:
                if connection is not None:
                    logger.debug("closing connection")
            except Exception as e:
                logger.error("Exception while closing connection: ", str(e))
                return False, str(e)
