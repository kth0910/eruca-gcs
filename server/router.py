# server/router.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse
from typing import List
import asyncio
import sqlite3
from collections import deque
from models import Telemetry
import os

router = APIRouter()

# SSE용 큐 (최대 200개 메시지 버퍼)
sse_queue = deque(maxlen=1000)   # ← 200 → 1000 (원한다면 더 크게)


# SQLite 연결 (main.py에서 테이블 초기화 후 사용)
conn = sqlite3.connect("telemetry.db", check_same_thread=False)
cursor = conn.cursor()

@router.get("/data", response_model=List[Telemetry])
def get_data(limit: int = 50):
    """
    최근 telemetry 레코드를 REST로 조회합니다.
    """
    cursor.execute(
        "SELECT topic, message, timestamp FROM telemetry "
        "ORDER BY timestamp DESC LIMIT ?", (limit,)
    )
    rows = cursor.fetchall()
    # Pydantic 모델로 반환
    return [Telemetry(topic=row[0], message=row[1], timestamp=row[2]) for row in rows]

async def event_generator():
    """
    SSE 이벤트를 비동기 스트리밍합니다.
    큐가 순환(overrun)되어 last_index가 앞서 나가더라도
    자동으로 현재 큐 끝으로 리셋해 주는 것이 핵심.
    """
    last_index = 0
    while True:
        await asyncio.sleep(0.1)

        # ➊ 큐가 순환해 last_index가 범위를 벗어난 경우 보정
        if last_index >= len(sse_queue):
            last_index = len(sse_queue)     # ← 현재 큐 끝으로 리셋

        # ➋ 새 메시지 전송
        while last_index < len(sse_queue):
            yield sse_queue[last_index]
            last_index += 1

        # ➌ 메시지가 없는 동안에도 15 초마다 ping 주석을 보내 연결 유지
        #    (브라우저 SSE 타임아웃 방지)
        if last_index == len(sse_queue):
            yield ":\n\n"
            
            

@router.get("/stream")
async def stream():
    """
    Server-Sent Events 엔드포인트
    """
    return StreamingResponse(event_generator(), media_type="text/event-stream")

BASE_DIR = os.path.dirname(__file__)

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    path = os.path.join(BASE_DIR, "static", "dashboard.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()