import pandas as pd
from information.plugins import get_information_api
from data import refresh_api


def valid_employment(sorted_logs):

    for log in sorted_logs:
        print(log)

    logs = {
        'Datetime': [],
        'Auditorium': [],
        'NumPerson': []
    }

    for log in sorted_logs:
        if 'Datetime' in log:
            logs['Datetime'].append(log['Datetime'])
        elif 'Auditorium' in log:
            logs['Auditorium'].append(log['Auditorium'])
        else:
            logs['NumPerson'].append(log['NumPerson'])

    datetime, auditorium, numperson = logs.values()
    return [(d, a, n) for d, a, n in zip(datetime, auditorium, numperson)]


def get_employment():

    refresh_api()
    api = get_information_api('api.json')

    sorted_logs = sorted(
        [inf for inf in api if 'topic' in inf and '_bot' not in inf],
        key=lambda log: log['time']
    )

    logs = valid_employment(sorted_logs)

    employment = pd.DataFrame(
        logs, columns=['datetime', 'auditorium', 'numperson']
    )

    return employment
