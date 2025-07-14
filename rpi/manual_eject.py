# rpi/manual_eject.py

import threading
from queue import Queue
import RPi.GPIO as GPIO
import time

from command_sender import send_command
from config       import BUTTON_PIN


# 이 lock 으로 시리얼 읽기(read_line)와 쓰기(send_command)를 보호합니다.
serial_lock = threading.Lock()

# 수동 사출 명령을 담을 큐
_cmd_queue = Queue()

# (1) GPIO 핸들러: 버튼 누르면 큐에 'EJECT' 삽입
def _button_callback(channel):
    print("[MANUAL] Button pressed, queueing EJECT")
    _cmd_queue.put("EJECT")

def init_manual():
    """
    GPIO 버튼 감지 및 워커 스레드 시작.
    """
    # 1) GPIO 초기화
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(
        BUTTON_PIN,
        GPIO.FALLING,
        callback=_button_callback,
        bouncetime=200
    )
    print(f"[MANUAL] GPIO {BUTTON_PIN} set up for manual eject")

    # 2) 워커 스레드: 큐에서 꺼내서 serial write
    def _worker(ser):
        while True:
            cmd = _cmd_queue.get()  # 블로킹
            if cmd == "EJECT":
                with serial_lock:
                    send_command(ser, cmd)
                print("[MANUAL] EJECT command sent")
            _cmd_queue.task_done()

    # 스레드를 시작(daemon)
    def start_worker(ser):
        t = threading.Thread(target=_worker, args=(ser,), daemon=True)
        t.start()
        print("[MANUAL] Worker thread started")

    return start_worker
