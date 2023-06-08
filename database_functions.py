from __future__ import annotations

from mysql import connector 
"""File with ready function to connect with database"""


def connect_to_db():
    connection = connector.connect(
        user = "student",
        password = "Student123",
        host = "127.0.0.1",
        database = "projekt_air",
        auth_plugin = "mysql_native_password"
    )
    return connection


def put_value_into_db(value: float, insert_query: str) -> None:
    connection = connect_to_db()
    cursor = connection.cursor()
    query = insert_query  % (value)
    cursor.execute(query)
    connection.commit()
    connection.close()
    