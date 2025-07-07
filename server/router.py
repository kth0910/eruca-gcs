# server/router.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import List
import asyncio
import sqlite3
from collections import deque
from .models import Telemetry

router = APIRouter()

# SSE용 큐 (최대 200개 메시지 버퍼)
sse_queue = deque(maxlen=200)

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
    """
    last_index = 0
    while True:
        await asyncio.sleep(0.1)
        while last_index < len(sse_queue):
            yield sse_queue[last_index]
            last_index += 1

@router.get("/stream")
async def stream():
    """
    Server-Sent Events 엔드포인트
    """
    return StreamingResponse(event_generator(), media_type="text/event-stream")