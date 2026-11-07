# 볼 부상 시스템 설정값
# 핀 번호는 BCM 번호. 저장소 루트 README.md 의 배선 요약과 같음.
# 장치에서 직접 재서 정해야 하는 값에는 "측정 필요" 라고 적어 둠.

# ---- 핀 ----
FAN_PIN = 18           # 물리 12번 핀
BALL_TRIG = 23         # HY-SRF05, 관 위에서 아래를 봄
BALL_ECHO = 24
HAND_TRIG = 17         # HC-SR04, 위를 봄 (손 높이)
HAND_ECHO = 27

# ---- 팬 ----
FAN_PWM_HZ = 100       # fan_test.py 와 같은 주파수
FAN_MIN = 0.30         # 측정 필요: fan_test.py 에서 팬이 다시 돌기 시작한 세기 (0~1)
FAN_HOVER = 0.60       # 측정 필요: 공이 관 가운데쯤 떠 있는 세기. PID 의 기본값으로 씀

# ---- 관 · 센서 위치 (cm) ----
BALL_SENSOR_HEIGHT = 50.0   # 측정 필요: 관 바닥(팬 위)에서 HY-SRF05 까지 높이
BALL_DIAMETER = 4.0         # 탁구공 지름
# 공 높이 = 관 바닥에서 공 아랫면까지. 0 이면 팬 위에 얹힌 상태.

# ---- 목표 높이 ----
# 손이 HC-SR04 위 HAND_NEAR~HAND_FAR 에 있으면 목표 높이를 TARGET_LOW~TARGET_HIGH 로 비례 대응
HAND_NEAR = 5.0
HAND_FAR = 40.0
TARGET_LOW = 5.0
TARGET_HIGH = 35.0     # 센서 바로 아래 2~3cm 는 초음파가 못 재므로 관 끝까지 올리지 않음

# ---- 제어 ----
LOOP_HZ = 20           # 제어 주기 (초당 횟수)
KP = 0.010             # 시작값. 단위는 「팬 세기 / cm」
KI = 0.004
KD = 0.015
D_FILTER = 0.3         # 미분 저역통과 계수 (0~1, 작을수록 부드러움)
I_LIMIT = 0.3          # 적분항이 팬 세기에 더할 수 있는 최대 크기

# ---- 안전 ----
MAX_MISSES = 10        # 공 거리를 연속 이만큼 못 재면 팬을 끔
