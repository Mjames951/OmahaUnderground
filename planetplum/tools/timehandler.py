import datetime

def currentDate():
    return (datetime.datetime.now() - datetime.timedelta(hours=5)).date()