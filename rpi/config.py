# rpi/config.py
import os

from dotenv import load_dotenv

# ───── 환경변수 로드 (.env 에 EC2_IP, EC2_PORT, MQTT_TOPIC, SERIAL_PORT, BAUD_RATE 정의) ─────
load_dotenv()
EC2_IP      = os.getenv("EC2_IP")
EC2_PORT    = int(os.getenv("EC2_PORT", 1883))
MQTT_TOPIC  = os.getenv("MQTT_TOPIC", "rpi")
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
BAUD_RATE   = int(os.getenv("BAUD_RATE", "115200"))
BUTTON_PIN = 17    # 물리 11
#LED_PIN    = 27    # 물리 13
