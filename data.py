import requests
import json


class ApiRightech:

    def __init__(self):
        self.init_security()


    def init_security(self):
        with open('content/information/security.json') as file:
            security = json.loads(file.read())
            self.token = security.get('token')
            self.path = security.get('path')


    def get_data_by_api(self):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.token)
        }

        self.api = requests.get(self.path, headers=headers)
        self.logs = json.loads(self.api.text)

        return self.logs


    def set_api_logs(self):
        with open('content/information/api.json', 'w') as file:
            json.dump(self.logs, file, ensure_ascii=False, indent=4)


apirightech = ApiRightech()
apirightech.get_data_by_api()
apirightech.set_api_logs()