import requests
import json


class ApiRightech:

    def __init__(self):
        self.init_security()


    def init_security(self):
        with open('content/logs/security.json') as file:
            security = json.loads(file.read())
            self.path = security.get('path')
            self.token = security.get('token')

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }

        self.api = requests.get(self.path, headers=headers)
        self.logs = json.loads(self.api.text)


    def set_api_logs(self):
        with open('content/logs/api.json', 'w') as file:
            json.dump(self.logs, file, ensure_ascii=False, indent=4)


def refresh_api():
    apirightech = ApiRightech()
    apirightech.set_api_logs()