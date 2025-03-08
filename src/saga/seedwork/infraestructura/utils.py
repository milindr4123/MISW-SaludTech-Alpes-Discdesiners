import time
import os
from datetime import datetime

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(fecha):
    """
    Convierte una fecha en formato datetime a milisegundos desde epoch.
    """
    if fecha is None:
        return 0
    try:
        epoch = datetime(1970, 1, 1)
    except Exception as e:
        print(e)
        
    return int((fecha - epoch).total_seconds() * 1000)

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def broker_host():
    return os.getenv('BROKER_HOST', default="localhost")
