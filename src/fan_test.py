# 팬 PWM 테스트: GPIO18(12번 핀) -> 1kΩ -> 2N2222 베이스
# 실행: python3 fan_test.py   (Ctrl+C로 종료)
from time import sleep
from gpiozero import PWMOutputDevice

fan = PWMOutputDevice(18, frequency=100)  # 100Hz 소프트웨어 PWM

try:
    print("1) 3초 동안 최대 속도")
    fan.value = 1.0
    sleep(3)

    print("2) 세기를 100%부터 10%씩 낮춰요. 팬이 멈추는 값을 적어 두세요.")
    for duty in range(100, -1, -10):
        fan.value = duty / 100
        print(f"   {duty}%")
        sleep(2)

    print("3) 다시 올려요. 팬이 멈춘 상태에서 다시 돌기 시작하는 값을 적어 두세요.")
    for duty in range(0, 101, 10):
        fan.value = duty / 100
        print(f"   {duty}%")
        sleep(2)
finally:
    fan.off()
    fan.close()
    print("끝")
