# 초음파 센서 2개 거리 확인 (팬은 켜지 않음)
# 실행: python3 sonar_test.py   (Ctrl+C로 종료)
# 공을 관 안에서 손으로 올렸다 내리고, 손을 HC-SR04 위에서 움직여 값이 따라오는지 보세요.
from time import sleep

import config
from sonar import Sonar

ball = Sonar(config.BALL_TRIG, config.BALL_ECHO)
hand = Sonar(config.HAND_TRIG, config.HAND_ECHO)


def fmt(cm):
    return "  못 읽음" if cm is None else f"{cm:6.1f}cm"


try:
    while True:
        b = ball.measure()
        sleep(0.02)
        h = hand.measure()
        print(f"공 센서 {fmt(b)}   손 센서 {fmt(h)}")
        sleep(0.2)
except KeyboardInterrupt:
    pass
finally:
    ball.close()
    hand.close()
    print("끝")
