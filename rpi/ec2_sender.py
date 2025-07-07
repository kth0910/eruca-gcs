# rpi/ec2_sender.py

import paho.mqtt.client as mqtt
from config import EC2_IP, EC2_PORT, MQTT_TOPIC

def init_mqtt():
    """
    MQTT 클라이언트를 생성·연결하고 loop를 백그라운드로 돌립니다.
    """
    client = mqtt.Client()
    client.connect(EC2_IP, EC2_PORT, keepalive=60)
    client.loop_start()
    return client

def send_message(client, message: str):
    """
    주어진 메시지를 미리 지정된 토픽으로 발행합니다.
    """
    client.publish(MQTT_TOPIC, message)
