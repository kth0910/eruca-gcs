# rpi/command_sender.py

import serial
import json

def send_command(ser, cmd: str):
    packet = {
        "type": "command",
        "cmd": cmd
    }
    ser.write((json.dumps(packet) + "\n").encode('utf-8'))
    print("[CMD] Sent:", cmd)
