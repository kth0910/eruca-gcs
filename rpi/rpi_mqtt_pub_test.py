import time
import random
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("EC2_ENDPOINT")

PORT = os.getenv("BROKER_PORT", 1883)
TOPIC = "rocket/sensors/accel"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    data = f"ACC:{random.randint(500, 700)},{random.randint(-50, 50)},{random.randint(15000, 16000)}"
    client.publish(TOPIC, data)
    print(f"Sent: {data}")
    time.sleep(0.1)
