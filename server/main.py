# server/main.py
import threading
import sqlite3
from datetime import datetime
import paho.mqtt.client as mqtt
import uvicorn
from fastapi import FastAPI
import os
from router import router, sse_queue

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

# 2) MQTT 콜백 정의
def on_connect(client, userdata, flags, rc):
    print("MQTT connected with code", rc)
    client.subscribe("rocket/sensors/#")


def on_message(client, userdata, msg):
    payload = msg.payload.decode(errors="ignore")
    # DB 저장
    conn = sqlite3.connect("telemetry.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO telemetry (topic, message, timestamp) VALUES (?, ?, ?)" ,
        (msg.topic, payload, datetime.now())
    )
    conn.commit()
    conn.close()
    # SSE 큐에 포맷 맞춰 추가
    sse_queue.append(f"data: {msg.topic}:{payload}\n\n")

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
