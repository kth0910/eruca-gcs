from queue import Queue
import threading
import time
import sys

from command_sender import send_command

serial_lock = threading.Lock()
_cmd_queue = Queue()

def init_manual():
    def _input_listener():
        print("[MANUAL] Press ENTER to send EJECT command")
        while True:
            try:
                line = sys.stdin.readline()
                if line.strip() == "":
                    print("[MANUAL] ENTER pressed, queuing EJECT")
                    _cmd_queue.put("EJECT")
            except Exception as e:
                print(f"[ERROR] Input listener failed: {e}")

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

    def start_worker(ser):
        threading.Thread(target=_worker, args=(ser,), daemon=True).start()
        threading.Thread(target=_input_listener, daemon=True).start()
        print("[MANUAL] Worker and input threads started")

    return start_worker

