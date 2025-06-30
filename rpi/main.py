# rpi/main.py

from serial_reader import open_serial, read_packet
from parser import parse_packet
from ec2_sender import send_to_server
from logger import log_data

def main():
    ser = open_serial()
    print("[*] Serial opened.")

    while True:
        raw = read_packet(ser)
        if raw:
            data = parse_packet(raw)
            if data:
                log_data(data)
                send_to_server(data)

if __name__ == "__main__":
    main()
