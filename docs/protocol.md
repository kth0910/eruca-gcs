---
title: 통신 구조 및 데이터 포맷
nav_order: 2
---

# 통신 구조 & 데이터 포맷

## 1. Mega → RPi (telemetry)
~~~json
{
  "type": "telemetry",
  "timestamp": 1720000012,
  "sequence": 42,
  "bmp280": {
    "altitude": 123.4,
    "temperature": 27.9
  },
  "mpu6050": {
    "accel": { "x": 0.01, "y": -0.01, "z": 9.80 },
    "gyro":  { "x": 0.00, "y": 0.00, "z": 0.01 }
  },
  "gps": {
    "lat": 37.123456,
    "lon": 127.456789,
    "altitude": 135.6
  }
}
~~~

## 2. RPi → Mega (command)
~~~json
{
  "type": "command",
  "cmd": "DEPLOY_PARACHUTE",
  "timestamp": 1720000050
}
~~~

## 3. Mega → RPi (ack)
~~~json
{
  "type": "ack",
  "cmd": "DEPLOY_PARACHUTE",
  "status": "OK",
  "timestamp": 1720000052
}
~~~
