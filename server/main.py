import sqlite3
from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from paho.mqtt.client import Client
import threading
from collections import deque
import asyncio

app = FastAPI()

# SQLite 초기화
conn = sqlite3.connect("telemetry.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# MQTT 콜백 함수
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("rocket/sensors/#")

# 최신 메시지를 저장하는 큐 (길이 제한 있음)
message_queue = deque(maxlen=100)

# 기존 MQTT on_message에 메시지 큐 추가
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received from {msg.topic}: {message}")
    cursor.execute("INSERT INTO telemetry (topic, message) VALUES (?, ?)", (msg.topic, message))
    conn.commit()
    message_queue.append(f"data: {msg.topic} - {message}\n\n")

# MQTT 스레드 실행
def mqtt_thread():
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.loop_forever()

threading.Thread(target=mqtt_thread, daemon=True).start()

# FastAPI 엔드포인트
@app.get("/data")
def get_data(limit: int = 50):
    cursor.execute("SELECT topic, message, timestamp FROM telemetry ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    return JSONResponse(content={"data": rows})

# SSE 엔드포인트
@app.get("/stream")
async def stream():
    async def event_generator():
        last_index = 0
        while True:
            await asyncio.sleep(0.5)
            if len(message_queue) > last_index:
                while last_index < len(message_queue):
                    yield message_queue[last_index]
                    last_index += 1
    return StreamingResponse(event_generator(), media_type="text/event-stream")