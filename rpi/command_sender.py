# rpi/command_sender.py

import serial
import json

def send_command(ser: serial.Serial, cmd: str):
    packet = {
        "type": "command",
        "cmd": cmd
    }
    ser.write("EJECT" + "\n").encode('utf-8'))
    print("[CMD] Sent:", cmd)
