import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    if isinstance(dt, int):
        return dt
    return (dt - epoch).total_seconds() * 1000.0