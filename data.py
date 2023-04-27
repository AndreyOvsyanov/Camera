import json
import requests

req = requests.get('https://dev.rightech.io/api/v1/objects/644580d1cee0790010607ca9/packets?withChildGroups=true&ofType=telemetry&snaps=true&nolimit=true&streamed=true&from=1682197200000&to=1682283599999&db=pgts')
print(req.text)