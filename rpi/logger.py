# rpi/logger.py

import csv
from datetime import datetime
import os

LOG_FILE = f"telemetry_{datetime.now().date()}.csv"

def log_data(data):
    fieldnames = list(data.keys())
    is_new_file = not os.path.exists(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if is_new_file:
            writer.writeheader()
        writer.writerow(data)
