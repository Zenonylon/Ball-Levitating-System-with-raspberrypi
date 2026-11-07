# PID 제어기
# - 미분은 측정값에 대해 계산 (목표가 바뀔 때 출력이 튀지 않음) + 저역통과
# - 적분항 크기를 제한하고, 출력이 포화되면 적분을 멈춤 (windup 방지)


class PID:
    def __init__(self, kp, ki, kd, out_min, out_max, i_limit, d_filter=1.0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.out_min, self.out_max = out_min, out_max
        self.i_limit = i_limit
        self.d_filter = d_filter
        self.reset()

    def reset(self):
        self.integral = 0.0
        self.d_term = 0.0
        self._last_meas = None

    def update(self, target, meas, dt):
        error = target - meas

        if self._last_meas is None:
            raw_d = 0.0
        else:
            raw_d = -(meas - self._last_meas) / dt
        self._last_meas = meas
        self.d_term += self.d_filter * (self.kd * raw_d - self.d_term)

        p_term = self.kp * error
        out = p_term + self.integral + self.d_term

        # 포화 상태에서 같은 방향으로 더 쌓이지 않을 때만 적분
        saturated_high = out >= self.out_max and error > 0
        saturated_low = out <= self.out_min and error < 0
        if not (saturated_high or saturated_low):
            self.integral += self.ki * error * dt
            self.integral = max(-self.i_limit, min(self.i_limit, self.integral))
            out = p_term + self.integral + self.d_term

        return max(self.out_min, min(self.out_max, out))
