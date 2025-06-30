# rpi/config.py
import os

from dotenv import load_dotenv
load_dotenv()

SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
BAUD_RATE = int(os.getenv("BAUD_RATE", "115200"))

EC2_ENDPOINT = os.getenv("EC2_ENDPOINT", "http://localhost/api/telemetry")
