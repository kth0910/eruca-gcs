# server/main.py
import threading
import sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt
import uvicorn
from fastapi import FastAPI
import os
from router import router, sse_queue
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(router)



# 1) 초기 DB 테이블 생성
def init_db():
    # DB 파일이 없으면 생성
    if not os.path.exists("telemetry.db"):
        open("telemetry.db", "a").close()
        
    conn = sqlite3.connect("telemetry.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

# ─── Static Files 설정 ───────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)


# 2) MQTT 콜백 정의
def on_connect(client, userdata, flags, rc):
    print("MQTT connected with code", rc)
    client.subscribe("rocket/sensors/#")


def on_message(client, userdata, msg):
    payload = msg.payload.decode(errors="ignore")
    print(f"[MQTT] {msg.topic}: {payload}")

    # DB 저장
    try:
        conn = sqlite3.connect("telemetry.db", check_same_thread=False)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO telemetry (topic, message, timestamp) VALUES (?, ?, ?)",
            (msg.topic, payload, datetime.now())
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return  # DB 삽입 실패 시 SSE 큐에도 추가하지 않음

    # 메시지 파싱 및 SSE 큐 추가
    try:
        # 기대하는 형식: "ACC:548,44,15140;GYRO:-193,-243,-104"
        if "ACC:" in payload and ";GYRO:" in payload:
            parts = payload.split("ACC:")
            accgyro = parts[1].split(";GYRO:")
            acc = accgyro[0].split(",")
            gyro = accgyro[1].split(",")
            if len(acc) == 3 and len(gyro) == 3:
                ax, ay, az = map(int, acc)
                gx, gy, gz = map(int, gyro)
                # 포맷이 완전한 경우에만 SSE 큐에 추가
                formatted = f"data: {msg.topic}: ACC:{ax},{ay},{az};GYRO:{gx},{gy},{gz}\n\n"
                sse_queue.append(formatted)
            else:
                print("[FORMAT WARNING] Invalid acc/gyro length")
        else:
            print("[FORMAT WARNING] Missing ACC or GYRO")
    except Exception as e:
        print(f"[PARSING ERROR] {e}")


# 3) 백그라운드에서 MQTT 구독 시작
def start_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    init_db()
    threading.Thread(target=start_mqtt_client, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
