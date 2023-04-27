import paho.mqtt.client as mqtt
from datetime import datetime
import time

class MQTTClient():

    def __init__(self, broker_address, port, client_id):

        self.connected = False
        self.broker_address = broker_address
        self.port = port
        self.client_id = client_id
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.on_connect
        self.client.connect(broker_address, port=port)
        self.client.loop_start()

    def publish_msg(self, data):
        try:
            while self.connected != True:
                for nameNode, value in data.items():
                    self.client.publish(nameNode, value)

                print("Сообщение отправлено")
                time.sleep(10)

        except KeyboardInterrupt as ki:
            self.client.disconnect()
            self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print('connected to broker')
            global connected
            connected = True
        else:
            print('connection failed')


mqttclient = MQTTClient(
    broker_address='dev.rightech.io',
    port=1883,
    client_id='andrey01109-drb9hf'
)

data = {
    'base/state/datetime':
        datetime.now().date().strftime("%d-%m-%y") + " " + datetime.now().time().strftime("%H:%M:%S"),
    'base/state/audit': 317,
    'base/state/numperson': 10
}

mqttclient.publish_msg(data)