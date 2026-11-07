# 초음파 거리 센서 (HY-SRF05, HC-SR04 공통, Trig/Echo 방식)
# Echo 는 1kΩ/2kΩ 분압으로 3.3V 로 낮춰서 연결.
# 두 센서가 서로의 소리를 듣지 않도록 한 번에 하나씩만 잼 (measure() 를 차례로 호출).
from threading import Event
from time import sleep

from gpiozero import GPIODevice

SPEED_OF_SOUND = 34326  # cm/s, 20°C


class Sonar:
    def __init__(self, trig, echo, max_cm=200):
        self._trig = GPIODevice(trig)
        self._trig.pin.function = 'output'
        self._trig.pin.state = False
        self._echo = GPIODevice(echo)
        self._echo.pin.function = 'input'
        self._echo.pin.pull = 'floating'
        self._echo.pin.edges = 'both'
        self._echo.pin.bounce = None
        self._echo.pin.when_changed = self._on_echo
        self._factory = self._echo.pin_factory
        self._done = Event()
        self._rise = None
        self._fall = None
        # 왕복 시간 + 여유 (소리가 안 돌아와도 센서가 Echo 를 내리는 데 걸리는 시간보다 짧게 잡지 않음)
        self._timeout = 2 * max_cm / SPEED_OF_SOUND + 0.01

    def _on_echo(self, ticks, state):
        if state:
            self._rise = ticks
        else:
            self._fall = ticks
            self._done.set()

    def measure(self):
        """거리(cm). 못 재면 None."""
        self._done.clear()
        self._rise = self._fall = None
        self._trig.pin.state = True
        sleep(0.00001)  # 10µs 이상 트리거 펄스
        self._trig.pin.state = False
        if not self._done.wait(self._timeout) or self._rise is None:
            return None
        dt = self._factory.ticks_diff(self._fall, self._rise)
        if dt <= 0:
            return None
        return dt * SPEED_OF_SOUND / 2

    def close(self):
        self._echo.close()
        self._trig.close()
