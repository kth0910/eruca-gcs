# rpi/main.py

import time
from serial_reader import init_serial, read_line
from ec2_sender   import init_mqtt, send_message

def debug_print(data: str):
    """
    디버그용 출력. 운영 시 이 호출부만 지우면 됩니다.
    """
    print(f"[DEBUG] {data}")

def main():
    ser         = init_serial()
    mqtt_client = init_mqtt()

    try:
        while True:
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
        mqtt_client.loop_stop()
        ser.close()

if __name__ == "__main__":
    main()
