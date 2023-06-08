from __future__ import annotations

from time import sleep
import serial

from database_functions import put_value_into_db
from measure_functions import get_value_from_measure


if __name__ == "__main__":
    ser = serial.Serial("COM6", 9600)
    
    while True:
        line = ser.readline().decode(encoding='latin-1').strip().split(" ")
        checker = line[0]  # if it is calibrating or test, do nothing
        
        if ":" in checker:
            value = get_value_from_measure(measure=checker)

        if "temperature" in checker:
            query = """INSERT INTO
                TEMPERATURE (TEMPERATURE) VALUES ((%s))"""  

            put_value_into_db(value, query)
            print("temperature:", value)

        if "humidity" in checker:
            query = """INSERT INTO
                  HUMIDITY (HUMIDITY) VALUES ((%s))""" 
                
            put_value_into_db(value, query)
            print("humidity:", value)
            
        if "LPG" in checker:
            if value > 0:  # just in situation, when sensor detect LPG measure is saved
                query = """INSERT INTO
                LPG (LPG) VALUES ((%s))"""
                
                put_value_into_db(value, query)
                print("LPG detected !, value from sensor:", value) 
            else:
                continue
            
        if "CO" in checker:
            if value > 0:  # just in situation, when sensor detect CO measure is saved
                query = """INSERT INTO
                CO (CO) VALUES ((%s))"""
            
                put_value_into_db(value, query)
                print("CO detected !, value from sensor:", value)
            else:
                continue
            
        if "SMOKE" in checker:
            if value > 0:  # just in situation, when sensor detect SMOKE measure is saved
                query = """INSERT INTO
                CO (CO) VALUES ((%s))"""
                
                put_value_into_db(value, query)
                print("SMOKE detected !, value from sensor: ", value)
            else:
                continue   
                   
        sleep(1)
