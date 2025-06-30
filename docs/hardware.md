---
title: 하드웨어 구성
nav_order: 3
---

# 환경 설정 & 보드 매핑

## Arduino Mega
- BMP280 (altitude, temperature)
- MPU6050
- GY6500
- NEO-6M GPS
- Serial에 연결된 XBee 실드

## Arduino Nano
- BMP280
- MPU6050
- NEO-6M GPS

## Raspberry Pi
- XBee USB 어댑터로 연결
- Python 기반 수신 및 전송 (pyserial, requests 등)

## EC2
- FastAPI
- Python 3.11
- Uvicorn
- Docker 및 docker-compose (선택)

## 사용 부품 요약
- XBee S2C 모듈
- XBee Arduino 실드 (핀 점퍼형 추천)
- XBee USB 어댑터 (RPi용)
