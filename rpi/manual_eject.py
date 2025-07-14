from gpiozero import Button
from queue import Queue
import threading
import time

from command_sender import send_command
from config import BUTTON_PIN

serial_lock = threading.Lock()
_cmd_queue = Queue()
_devices = {}

def init_manual():
    button = Button(BUTTON_PIN)
    _devices["button"] = button
    
    def _on_press():
        print("[MANUAL] Button pressed, queuing EJECT")
        _cmd_queue.put("EJECT")

    def _worker(ser):
        while True:
            cmd = _cmd_queue.get()
            try:
                if cmd == "EJECT":
                    with serial_lock:
                        send_command(ser, cmd)
                    print("[MANUAL] EJECT command sent")
                    time.sleep(0.2)
            except Exception as e:
                print(f"[ERROR] Failed to send command: {e}")
            finally:
                _cmd_queue.task_done()
            

    button.when_pressed = _on_press

    def start_worker(ser):
        t = threading.Thread(target=_worker, args=(ser,), daemon=True)
        t.start()
        print("[MANUAL] Worker thread started")

    return start_worker


def cleanup():
    for dev in _devices.values():
        dev.close()