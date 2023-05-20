import datetime
import json
import time

from datetime import datetime

SHAPE = (640, 480)


def get_name_folder():
    today = datetime.datetime.today()
    return str(today.date()) + "_" + str(today.hour) + "-" + str(today.minute) + "-" + str(today.second)


def get_information_api(path):
    with open('content/logs/{}'.format(path)) as file:
        api = json.loads(file.read())

    return api


def get_current_datetime():
    return datetime.now().date().strftime("%d-%m-%y") + " " + datetime.now().time().strftime("%H:%M:%S")


def init_security():
    with open('content/logs/security.json') as file:
        security = json.loads(file.read())

    security['path'] = "https://dev.rightech.io/api/v1/objects/645fd273858b98a72bb920a0/" \
                        "packets?withChildGroups=true" \
                        "&ofType=telemetry" \
                        "&snaps=true" \
                        "&nolimit=true" \
                        "&streamed=true" \
                        "&from={}000" \
                        "&db=pgts".format(int(time.time()))

    with open('content/logs/security.json', 'w') as file:
        json.dump(security, file, ensure_ascii=False, indent=4)


