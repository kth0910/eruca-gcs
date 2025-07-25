# rpi/main.py

import time
from serial_reader import init_serial, read_line
from ec2_sender   import init_mqtt, send_message
#from manual_eject_rpi import init_manual, serial_lock, cleanup
from manual_eject_pc import init_manual, serial_lock


def debug_print(data: str):
    """
    디버그용 출력. 운영 시 이 호출부만 지우면 됩니다.
    """
    print(f"[DEBUG] {data}")

def main():
    ser         = init_serial()
    
    # ─────────── 수동 사출 로직 초기화 ───────────
    start_manual = init_manual()
    start_manual(ser)   # Worker 스레드 기동
    # ────────────────────────────────────────────

    if ser:
        print("시리얼 포트 연결 성공:", ser.name)
    mqtt_client = init_mqtt()

    try:
        while True:
            if ser.in_waiting > 0:
                with serial_lock:
                    raw = read_line(ser)
                if not raw:
                    continue

                # 1) 디버그 출력
                debug_print(raw)

                # 2) EC2로 발행
                send_message(mqtt_client, raw)

            # 너무 빡빡한 루프 방지
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("종료 중...")
    finally:
        #cleanup()
        #print("[main] GPIO Cleanup completed.")
        mqtt_client.loop_stop()
        print("mqtt loop stopped.")
        ser.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()
