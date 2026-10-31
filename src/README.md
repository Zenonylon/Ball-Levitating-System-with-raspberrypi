# src

Raspberry Pi 4B 에서 실행하는 코드를 둠. 핀 배치는 저장소 루트 `README.md` 의 배선 요약을 따름.
필요한 패키지는 Raspberry Pi OS 에 기본으로 깔린 `gpiozero` 하나뿐임.

| 파일 | 내용 |
|---|---|
| `config.py` | 핀, 팬 최소 · 기본 세기, 관 높이, PID 계수 등 모든 설정값 |
| `fan.py` | 팬 PWM 구동 (최소 세기 아래로는 내려가지 않음) |
| `sonar.py` | 초음파 센서 거리 측정 (Trig/Echo, 한 번에 하나씩) |
| `pid.py` | PID 제어기 (측정값 미분, 적분 제한) |
| `levitate.py` | 본 프로그램: 손 높이를 목표로 공 높이를 PID 로 유지 |
| `fan_test.py` | 팬 단독 시험 (세기를 10% 씩 내렸다 올림) |
| `sonar_test.py` | 센서 2 개 거리 확인 (팬은 켜지 않음) |

## 실행 순서

`src/` 폴더에서 차례로 실행함. 모두 Ctrl+C 로 끝내고, 끝나면 팬이 꺼짐.

1. `python3 fan_test.py` — 팬이 다시 돌기 시작한 세기를 `config.py` 의 `FAN_MIN` 에 적음
2. `python3 sonar_test.py` — 두 센서 값이 손 · 공을 따라 바뀌는지 확인
3. `config.py` 의 `BALL_SENSOR_HEIGHT` 에 관 바닥(팬 위)에서 HY-SRF05 까지 높이를 적음
4. `python3 levitate.py --target 20` — 목표 고정으로 PID 를 맞춤.
   공이 겨우 떠 있는 팬 세기를 찾아 `FAN_HOVER` 에 적고, `--kp --ki --kd` 로 계수를 바꿔 가며 시험.
   `--log run1.csv` 를 붙이면 시간 · 목표 · 높이 · 팬 세기가 CSV 로 남음
5. `python3 levitate.py` — 손을 HC-SR04 위에서 올리고 내려 공이 따라오는지 확인

공 거리를 연속 10 번 못 읽으면 팬을 끄고 종료함.

## PID 튜닝 요령

1. `--ki 0 --kd 0` 으로 시작해 `--kp` 를 올림. 공이 목표 근처에서 위아래로 계속 흔들리기 시작하는 값의 절반쯤을 씀
2. `--kd` 를 올려 흔들림을 줄임
3. 목표보다 늘 조금 낮거나 높게 머물면 `--ki` 를 조금씩 올림
