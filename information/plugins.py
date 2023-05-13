import datetime
import json

SHAPE = (640, 480)


def get_name_folder():
    today = datetime.datetime.today()
    return str(today.date()) + "_" + str(today.hour) + "-" + str(today.minute) + "-" + str(today.second)


def get_information_api(path):
    with open('content/logs/{}'.format(path)) as file:
        api = json.loads(file.read())

    return api

