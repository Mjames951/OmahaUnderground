import datetime

def currentDate():
    return (datetime.datetime.now() - datetime.timedelta(hours=5)).date()

def datePlus(days):
    return (datetime.datetime.now() + datetime.timedelta(days=days)).date()


