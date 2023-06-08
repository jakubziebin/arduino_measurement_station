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


def reset_tables(values_to_reset: tuple) -> None:
    for value in values_to_reset:
        connection = connect_to_db()
        cursor = connection.cursor()
        query = f"""TRUNCATE TABLE {value}"""
        cursor.execute(query)
        connection.commit()
        connection.close()


def select_max_value(value: str) -> float | str:
    connection = connect_to_db()
    cursor = connection.cursor()
    query = f"""SELECT MAX({value}) FROM {value}"""
    cursor.execute(query)
    result = cursor.fetchone()
    connection.close()
    return result[0]
