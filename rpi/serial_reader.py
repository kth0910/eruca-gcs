# rpi/serial_reader.py

import serial
from config import SERIAL_PORT, BAUD_RATE

def init_serial():
    """
    시리얼 포트를 열어서 Serial 객체를 리턴합니다.
    """
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    return ser

def read_line(ser):
    """
    한 줄을 읽어 UTF-8로 디코딩한 뒤 strip() 처리하여 리턴합니다.
    문제가 생기면 None 리턴.
    """
    try:
        raw = ser.readline().decode("utf-8", errors="replace").strip()
        return raw or None
    except Exception:
        return None
