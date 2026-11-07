# DC 팬 PWM 구동: GPIO18 -> 1kΩ -> 2N2222 베이스
from gpiozero import PWMOutputDevice

import config


class Fan:
    def __init__(self, pin=config.FAN_PIN, frequency=config.FAN_PWM_HZ,
                 minimum=config.FAN_MIN):
        self._pwm = PWMOutputDevice(pin, frequency=frequency)
        self.minimum = minimum

    @property
    def duty(self):
        return self._pwm.value

    def set(self, duty):
        """duty 0~1. 0 보다 크면 팬이 멈추지 않도록 최소 세기 이상으로 올림."""
        duty = max(0.0, min(1.0, duty))
        if 0 < duty < self.minimum:
            duty = self.minimum
        self._pwm.value = duty

    def off(self):
        self._pwm.off()

    def close(self):
        self._pwm.off()
        self._pwm.close()
