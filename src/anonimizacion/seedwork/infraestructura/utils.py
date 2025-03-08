import time
import os
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(fecha):
    """
    Convierte una fecha en formato datetime a milisegundos desde epoch.
    """
    if fecha is None:
        return 0
    epoch = datetime(1970, 1, 1)
    return int((fecha - epoch).total_seconds() * 1000)

def millis_a_datetime(millis):
    if isinstance(millis, datetime.datetime):
        return millis
    elif isinstance(millis, (int, float)):
        return datetime.datetime.fromtimestamp(millis / 1000.0)
    else:
        raise TypeError("El valor debe ser un datetime o un número (int o float)")


def broker_host():
    return os.getenv('BROKER_HOST', default="localhost")
