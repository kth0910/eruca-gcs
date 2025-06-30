# rpi/serial_reader.py

import serial
from config import SERIAL_PORT, BAUD_RATE

def open_serial():
    return serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

def read_packet(ser):
    if ser.in_waiting:
        raw = ser.readline().decode('utf-8').strip()
        return raw
    return None
