# Useful tutorial for working with DB: https://pynative.com/python-postgresql-tutorial/

import psycopg2
from psycopg2 import extras


def execute_statement(statement):
    connection = None
    try:
        connection = psycopg2.connect(user='dev_course_user',
                                      password='pswd1234JAN!2024',
                                      host='207.180.203.217',
                                      port=5432,
                                      database='dev_course')
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(statement)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as error:
        return None
    finally:
        if connection:
            connection.close()
