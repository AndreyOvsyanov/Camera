import datetime

SHAPE = (640, 480)

def get_name_folder():
    today = datetime.datetime.today()
    return str(today.date()) + "_" + str(today.hour) + "-" + str(today.minute) + "-" + str(today.second)