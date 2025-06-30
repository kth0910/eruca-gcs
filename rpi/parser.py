# rpi/parser.py

import json

def parse_packet(raw_data):
    try:
        data = json.loads(raw_data)
        return data
    except json.JSONDecodeError:
        print("[!] JSON Parse Error:", raw_data)
        return None
