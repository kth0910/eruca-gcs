# rpi/ec2_sender.py

import requests
from config import EC2_ENDPOINT

def send_to_server(data):
    try:
        res = requests.post(EC2_ENDPOINT, json=data)
        print(f"[EC2] Sent: {res.status_code}")
    except Exception as e:
        print("[EC2] Error:", e)
