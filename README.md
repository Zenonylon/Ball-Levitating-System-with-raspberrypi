# Ball-Levitating-System-with-raspberrypi

45 mm 아크릴관 안의 탁구공을 팬 바람으로 띄우고, 관 옆에서 손을 올리고 내린 높이를 따라 공 높이를 제어하는 시스템임.
임베디드시스템설계 기말 프로젝트이며, 형상관리는 지도교수 가이드라인 (https://yongsoojoo.github.io/esd2026-agent-workflow/) 을 참고함.

## 구성

| 부품 | 역할 | 전원 |
|---|---|---|
| Raspberry Pi 4B | 센서를 읽고 PID 로 팬 세기를 계산 | USB-C 5 V 3 A 어댑터 |
| DC 팬 (5 V) | 관 아래에서 위로 바람을 보내 공을 띄움 | 18650 ×2 → MB102 5 V 출력 |
| 2N2222 + 1 kΩ | Pi PWM 신호로 팬 전류를 스위칭 | — |
| 1N4148 | 팬 역기전력으로부터 트랜지스터 보호 | — |
| HY-SRF05 | 관 위에서 아래로 공까지 거리 측정 | Pi 5 V |
| HC-SR04 | 위를 향해 손까지 거리 측정 → 목표 높이 | Pi 5 V |
| 1 kΩ + 2 kΩ ×2 | 센서 Echo 5 V → 3.3 V 분압 | — |

Pi 와 팬은 전원을 따로 받고 GND 만 공통으로 묶음.

## 배선 요약

핀 번호는 40 핀 헤더의 물리 번호, 괄호는 BCM 번호임.

| 신호 | Pi 핀 | 비고 |
|---|---|---|
| 팬 PWM | 12 (GPIO18) | 1 kΩ → 2N2222 베이스, 하드웨어 PWM |
| HY-SRF05 Trig | 16 (GPIO23) | 직접 연결 |
| HY-SRF05 Echo | 18 (GPIO24) | 1 kΩ 직렬, 18 번 핀 쪽에서 2 kΩ → GND |
| HC-SR04 Trig | 11 (GPIO17) | 직접 연결 |
| HC-SR04 Echo | 13 (GPIO27) | 1 kΩ 직렬, 13 번 핀 쪽에서 2 kΩ → GND |
| 센서 VCC | 2, 4 (5 V) | |
| GND | 6, 9, 14 | 14 번은 MB102 GND 와 공통 |

## 폴더

```
src/            Raspberry Pi 코드 (센서 읽기, 팬 PWM, 제어 루프)
daily-report/   하루 한 편의 작업 기록 (YYYY-MM-DD.md, 양식은 TEMPLATE.md)
```
