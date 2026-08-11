import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    def __init__(self, test_mode=False):
        self.connection = None
        self.test_mode = test_mode

    def connect(self, database_name=None):
        if database_name is None:
            env_var = "TEST_DATABASE_NAME" if self.test_mode else "DATABASE_NAME"
            database_name = os.environ.get(env_var)

        self.connection = psycopg2.connect(
            dbname=database_name,
            user=os.environ.get("DATABASE_USERNAME"),
            password=os.environ.get("DATABASE_PASSWORD"),
        )

    def execute(self, query, params=None):
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params or [])
        try:
            result = cursor.fetchall()
        except psycopg2.ProgrammingError:
            result = None
        self.connection.commit()
        cursor.close()
        return result

    def seed(self, sql_filename):
        with open(sql_filename, "r") as f:
            with self.connection.cursor() as cursor:
                cursor.execute(f.read())
        self.connection.commit()

    def close(self):
        self.connection.close()
