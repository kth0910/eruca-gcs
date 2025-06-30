---
title: 개요
nav_order: 1
---

# GCS-Groundstation 과정 설명

과정은 로켓의 도출시간 데이터를 XBee를 통해 수집하고, RPi를 통해 EC2 서버에 전송하고, FastAPI + Chart.js를 이용해 실시간 시각화하는 지상국 관제 시스템이다.

## 노드 역할
- Arduino Mega: 메인 센서 수집 + RPi 전송
- Arduino Nano: 보조 센서 수집 및 Mega에 전달
- Raspberry Pi: XBee로 데이터 수신 + EC2 전송 + 명령 수신 및 송신
- EC2: FastAPI 기반 데이터 API + 시각화 서버
- Frontend: HTML + Chart.js / Three.js 시각화
