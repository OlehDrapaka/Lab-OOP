import time
import json
import requests
import paho.mqtt.client as mqtt
from websocket import create_connection

BROKER_ADDRESS = "broker.hivemq.com"
BROKER_PORT = 1883
TOPIC = "device/mark"
MESSAGE = "telephone, pixel"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Підключено до MQTT брокера")
    else:
        print(f"Помилка підключення, код {rc}")

def on_publish(client, userdata, mid):
    print(f"Повідомлення успішно опубліковано (mid={mid}")

def on_disconnect(client, userdata, rc):
    print("Відключено від MQTT брокера")


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=60)
client.loop_start()

time.sleep(1)

result = client.publish(TOPIC, MESSAGE, qos=0, retain=False)
result.wait_for_publish()

print(f"Опубліковано в тему '{TOPIC}':{MESSAGE}")

time.sleep(1)
client.disconnect()
client.loop_stop()





class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        response = requests.get(f"{self.base_url}/{endpoint}")
        if response.status_code == 200:
            return response.json()
        return {"error": f"Помилка {response.status_code}"}


class WebSocketClient:
    def __init__(self):
        self.ws = None

    def connect(self, url):
        try:
            self.ws = create_connection(url)
            print(f"З'єднання з {url} успішно встановлено")
        except Exception as e:
            print(f"Помилка з'єднання WS: {e}")

    def send_message(self, message):
        if self.ws:
            try:
                self.ws.send(message)
                print(f"Відправлено (WS): {message}")
            except Exception as e:
                print(f"Помилка при відправці повідомлення: {e}")
        else:
            print("Помилка: Немає активного з'єднання WS.")

    def close(self):
        if self.ws:
            self.ws.close()


class MQTTClient:
    def __init__(self, broker, topic):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.broker = broker
        self.topic = topic

        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Підключено до MQTT брокера")
        else:
            print(f"Помилка підключення MQTT, код {rc}")

    def on_publish(self, client, userdata, mid):
        print(f"Повідомлення успішно опубліковано (mid={mid})")

    def on_disconnect(self, client, userdata, rc):
        print("Відключено від MQTT брокера")

    def connect(self):
        self.client.connect(self.broker, 1883, keepalive=60)
        self.client.loop_start()

    def publish(self, message):
        result = self.client.publish(self.topic, message, qos=0, retain=False)
        result.wait_for_publish()
        print(f"Опубліковано в тему '{self.topic}'")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()


class MultiProtocolHandler:
    def __init__(self, rest_client, ws_client, mqtt_client):
        self.rest_client = rest_client
        self.ws_client = ws_client
        self.mqtt_client = mqtt_client

    def process(self):
        print("\n--- Початок обробки даних ---")

        data_dict = self.rest_client.get("posts/1")
        print(f"REST: {data_dict}")
        data_str = json.dumps(data_dict)

        self.ws_client.send_message(data_str)

        self.mqtt_client.publish(data_str)

        print("--- Завершення обробки даних ---\n")


if __name__ == "__main__":
    BROKER_ADDRESS = "broker.hivemq.com"
    TOPIC = "device/mark"
    WS_URL = "wss://ws.postman-echo.com/raw"
    REST_URL = "https://jsonplaceholder.typicode.com"

    r_client = RestClient(REST_URL)

    m_client = MQTTClient(BROKER_ADDRESS, TOPIC)
    m_client.connect()

    w_client = WebSocketClient()
    w_client.connect(WS_URL)

    time.sleep(1)

    handler = MultiProtocolHandler(r_client, w_client, m_client)

    handler.process()

    time.sleep(1)
    m_client.disconnect()
    w_client.close()
    print("Програму успішно завершено.")