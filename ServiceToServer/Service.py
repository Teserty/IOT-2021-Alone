import requests
import time
import json
from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 1883
client_id = f'0'
worker_id = f'1'
sensors_per=[]
subscriber = mqtt_client.Client('0')
publisher = mqtt_client.Client('1')


def publish(client):
    val = requests.post("http://localhost:5000/")
    global sensors_per
    sensors_per = val.json()
    print("Sended " + json.dumps(sensors_per))
    result = client.publish("vmk/team_4/r", json.dumps(sensors_per))


def publish_loop(client):
    while True:
        publish(client)
        time.sleep(60)


def subscribe(client):
    def on_message(client, userdata, msg):
        print("OK")
        publish(publisher)
    client.subscribe("vmk/team_4/c")
    client.on_message = on_message


def run():
    import threading
    subscriber.connect(broker, port)
    publisher.connect(broker, port)
    subscribe(subscriber)
    thread1 = threading.Thread(target=subscriber.loop_forever)
    thread1.start()
    publisher.loop_start()
    publish_loop(publisher)


def exec():
    run()


if __name__ == "__main__":
    exec()
