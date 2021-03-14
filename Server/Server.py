import telebot
import time
import json

from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-0'
worker_id = f'python-mqtt-1'
# generate client ID with pub prefix randomly
# username = 'emqx'
# password = 'public'


import telebot
bot = telebot.TeleBot('1665454110:AAFPhm8SLBC8zs27LP9ApllC_p4E5bGFa7c')


time = "1 минуту"
command = "status"
mybots = [403938354]
sensors_per = []
subscriber = mqtt_client.Client('2')
publisher = mqtt_client.Client('3')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global bot
    print(message.chat.id)
    mybots.append(message.chat.id)
    bot.send_message(message.chat.id, f'Я бот для теплицы. Приятно познакомиться, я буду присылать сообщение о состоянии теплицы '
    f'раз в ' + time + '. Если хотите получить состояние в произволтный момент времение, пожалуйста, просто напишите '
                       '"' + command + '".')


@bot.message_handler(commands=['status'])
def send_status(message):
    publish(publisher)


def send_later():
    for id in mybots:
        print(sensors_per)
        bot.send_message(id, text=status_text())


def status_text():
    id = sensors_per[0].get('sensorID')
    value = sensors_per[0].get('value')
    type_sensor = sensors_per[0].get('typeSensor')
    return 'Состояния датчиков: id - {}, тип сенсора - {}, значение - {}'.format(id, type_sensor, value)


def run_bot():
    bot.polling(none_stop=True)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        from ast import literal_eval
        data = literal_eval(msg.payload.decode('utf8'))
        global sensors_per
        sensors_per = data
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        #print(data)
        send_later()
    client.subscribe("vmk/team_4/r")
    client.on_message = on_message


def publish(client):
    message = {"Request": "Data"}
    client.publish("vmk/team_4/c", json.dumps(message))


def run():
    import threading
    subscriber.connect(broker, port)
    subscribe(subscriber)
    publisher.connect(broker, port)
    publisher.loop_start()
    thread1 = threading.Thread(target=publish, args=[publisher])
    thread1.start()
    thread2 = threading.Thread(target=run_bot)
    thread2.start()
    subscribe(subscriber)
    subscriber.loop_forever()


def exec():
    run()


if __name__ == "__main__":
    exec()

