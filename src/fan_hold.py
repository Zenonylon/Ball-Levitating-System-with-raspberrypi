# 팬을 정한 세기로 계속 돌림 (공이 뜨는지 볼 때)
# 실행: python3 fan_hold.py        100%
#       python3 fan_hold.py 60     60%
# Ctrl+C로 종료
import sys
from signal import pause
from gpiozero import PWMOutputDevice

duty = float(sys.argv[1]) if len(sys.argv) > 1 else 100
fan = PWMOutputDevice(18, frequency=100)

try:
    fan.value = max(0, min(100, duty)) / 100
    print(f"팬 {fan.value * 100:.0f}% 로 도는 중 (Ctrl+C로 종료)")
    pause()
except KeyboardInterrupt:
    pass
finally:
    fan.off()
    fan.close()
    print("끝")
