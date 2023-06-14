from __future__ import annotations

from datetime import datetime, time
from time import sleep
import serial

from Adafruit_IO import Client

from database_functions import put_value_into_db, reset_tables, select_max_value
from measure_functions import get_value_from_measure


if __name__ == "__main__":
    ser = serial.Serial("COM6", 9600)

    ADAFRUIT_IO_USERNAME = 'ziebjak'
    ADAFRUIT_IO_KEY = '' 


    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    temperature_feed = aio.feeds("temperature")
    humidity_feed = aio.feeds("humidity")
    co_feed = aio.feeds("co")
    lpg_feed = aio.feeds("lpg")
    smoke_feed = aio.feeds("smoke")
    max_temp_feed = aio.feeds('todays-max-temperature')
    max_hum_feed = aio.feeds("todays-max-humidity")
    light_feed = aio.feeds("light")
    noise_feed = aio.feeds("noise")
    particles_feed = aio.feeds("particles")

    while True:

        line = ser.readline().decode(encoding='latin-1').strip().split(" ")
        checker = line[0]  # if it is calibrating or test, do nothing

        if ":" in checker:
            value = get_value_from_measure(measure=checker)

        if "PARTICLES" in checker:
            query = """INSERT INTO
                PARTICLES (PATRICLES) VALUES ((%s))""" 
            aio.send_data(particles_feed.key, value)
            put_value_into_db(value, query)
            print("particles:", value)

        if "temperature" in checker:
            query = """INSERT INTO
                TEMPERATURE (TEMPERATURE) VALUES ((%s))"""  

            aio.send_data(temperature_feed.key, value)
            put_value_into_db(value, query)
            print("temperature:", value)

        if "humidity" in checker:
            query = """INSERT INTO
                  HUMIDITY (HUMIDITY) VALUES ((%s))""" 
            
            aio.send_data(humidity_feed.key, value)
            put_value_into_db(value, query)
            print("humidity:", value)
            
        if "LPG" in checker:
            if value > 0:  # just in situation, when sensor detect LPG measure is saved
                query = """INSERT INTO
                LPG (LPG) VALUES ((%s))"""
                
                aio.send_data(lpg_feed.key, value)
                put_value_into_db(value, query)
                print("LPG detected !, value from sensor:", value) 
            else:
                continue
            
        if "CO" in checker:
            if value > 0:  # just in situation, when sensor detect CO measure is saved
                query = """INSERT INTO
                CO (CO) VALUES ((%s))"""

                aio.send_data(co_feed.key, value)
                put_value_into_db(value, query)
                print("CO detected !, value from sensor:", value)
            else:
                continue
            
        if "SMOKE" in checker:
            if value > 0:  # just in situation, when sensor detect SMOKE measure is saved
                query = """INSERT INTO
                CO (CO) VALUES ((%s))"""
                
                aio.send_data(smoke_feed.key, value)
                put_value_into_db(value, query)
                print("SMOKE detected !, value from sensor: ", value)
            else:
                continue   
        
        if "LIGHT" in checker:
            aio.send_data(light_feed.key, value)
            print("Light sent!")
        
        if "NOISE" in checker:
         aio.send_data(noise_feed.key, value)
         print("Noise sent!")
      

        if datetime.now().time() == time(0, 0):
            values_to_reset = ("temperature", "humidity", "LPG", "CO", "SMOKE")
            reset_tables(values_to_reset)
            print("Tables cleared ! Next save -> 00:01")

        highest_temperature = select_max_value("TEMPERATURE")
        highest_humidity = select_max_value("HUMIDITY")

        aio.send_data(max_temp_feed.key, highest_temperature)
        aio.send_data(max_hum_feed.key, highest_humidity)
        
        sleep(10)
