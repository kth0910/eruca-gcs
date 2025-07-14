# rpi/command_sender.py

import serial

def send_command(ser: serial.Serial, cmd: str):
    line = f"{cmd}\n"   
    ser.write(line.encode())   # 먼저 encode → bytes
    ser.flush()
    print("[CMD] Sent:", cmd)
