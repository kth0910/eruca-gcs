# server/models.py
from pydantic import BaseModel
from datetime import datetime

class Telemetry(BaseModel):
    topic: str
    message: str
    timestamp: datetime