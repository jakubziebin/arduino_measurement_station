from __future__ import annotations

from time import sleep
import serial

from connect_to_db import connect_to_db
from used_functions import get_value_from_measure


if __name__ == "__main__":
    while True:
        ser = serial.Serial("COM6", 9600)

        while True:
            line = ser.readline().decode(encoding='latin-1').strip().split(" ")
            checker = line[0]  # if it is calibrating or test, do nothing
            
            if "temperature" in checker:
                value = get_value_from_measure(measure=checker)

                connection = connect_to_db()
                cursor = connection.cursor()
                query = """INSERT INTO
                  TEMPERATURE (TEMPERATURE) VALUES ((%s))"""  % (value)
                cursor.execute(query)
                connection.commit()
                connection.close()
                
                print(value)

            if "humidity" in checker:
                value = get_value_from_measure(measure=checker)
                
                connection = connect_to_db()
                cursor = connection.cursor()

                query = """INSERT INTO
                  HUMIDITY (HUMIDITY) VALUES ((%s))"""  % (value)
                cursor.execute(query)
                connection.commit()
                connection.close()
            
            if "LPG" in checker:
                value = get_value_from_measure(measure=checker)
                if value == 0:
                    connection = connect_to_db()
                    cursor = connection.cursor()

                    query = """INSERT INTO
                  LPG (LPG) VALUES ((%s))"""  % (value)
                    cursor.execute(query)
                    connection.commit()
                    connection.close()
                else:
                    continue
            
            if "CO" in checker:
                    if value == 0:
                        connection = connect_to_db()
                        cursor = connection.cursor()

                        query = """INSERT INTO
                        CO (CO) VALUES ((%s))"""  % (value)
                        cursor.execute(query)
                        connection.commit()
                        connection.close()
                    else:
                        continue
            
            if "SMOKE" in checker:
                if value == 0:
                    connection = connect_to_db()
                    cursor = connection.cursor()

                    query = """INSERT INTO
                    CO (CO) VALUES ((%s))"""  % (value)
                    cursor.execute(query)
                    connection.commit()
                    connection.close()
                else:
                    continue   
                   


            sleep(5)
