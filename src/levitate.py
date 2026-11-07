# 볼 부상 PID 제어
# HY-SRF05 로 공 높이를 재고, HC-SR04 로 잰 손 높이를 목표로 삼아 팬 세기를 조절함.
#
# 실행 예:
#   python3 levitate.py                     손 높이를 따라감
#   python3 levitate.py --target 20         목표 높이 20cm 고정 (PID 튜닝할 때)
#   python3 levitate.py --kp 0.012 --log run1.csv
# Ctrl+C 로 종료하면 팬이 꺼짐.
import argparse
import csv
from time import monotonic, sleep

import config
from fan import Fan
from pid import PID
from sonar import Sonar


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def hand_to_target(hand_cm):
    """손까지 거리(cm) -> 목표 공 높이(cm). 범위를 벗어난 손은 None."""
    if hand_cm is None or hand_cm > config.HAND_FAR * 1.5:
        return None
    ratio = (hand_cm - config.HAND_NEAR) / (config.HAND_FAR - config.HAND_NEAR)
    ratio = clamp(ratio, 0.0, 1.0)
    return config.TARGET_LOW + ratio * (config.TARGET_HIGH - config.TARGET_LOW)


def ball_height(dist_cm):
    """센서~공 윗면 거리(cm) -> 관 바닥~공 아랫면 높이(cm)."""
    return config.BALL_SENSOR_HEIGHT - dist_cm - config.BALL_DIAMETER


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', type=float, help='목표 높이 cm 고정 (손 센서 안 씀)')
    ap.add_argument('--kp', type=float, default=config.KP)
    ap.add_argument('--ki', type=float, default=config.KI)
    ap.add_argument('--kd', type=float, default=config.KD)
    ap.add_argument('--hover', type=float, default=config.FAN_HOVER)
    ap.add_argument('--log', help='CSV 로 기록할 파일 이름')
    args = ap.parse_args()

    fan = Fan()
    ball = Sonar(config.BALL_TRIG, config.BALL_ECHO, max_cm=config.BALL_SENSOR_HEIGHT + 10)
    hand = None if args.target is not None else Sonar(config.HAND_TRIG, config.HAND_ECHO)

    # PID 출력은 기본 세기(hover)에 더하는 보정값
    pid = PID(args.kp, args.ki, args.kd,
              out_min=config.FAN_MIN - args.hover, out_max=1.0 - args.hover,
              i_limit=config.I_LIMIT, d_filter=config.D_FILTER)

    log_file = open(args.log, 'w', newline='') if args.log else None
    log = csv.writer(log_file) if log_file else None
    if log:
        log.writerow(['t', 'target_cm', 'height_cm', 'duty', 'p', 'i', 'd'])

    period = 1.0 / config.LOOP_HZ
    target = args.target if args.target is not None else config.TARGET_LOW
    height = None
    misses = 0
    t0 = next_tick = monotonic()
    last_print = 0.0

    print(f"Kp={args.kp} Ki={args.ki} Kd={args.kd} hover={args.hover}  (Ctrl+C 로 종료)")
    try:
        while True:
            if hand is not None:
                new_target = hand_to_target(hand.measure())
                if new_target is not None:
                    target += 0.2 * (new_target - target)  # 손 떨림이 바로 팬에 전해지지 않게
                sleep(0.005)  # 손 센서 메아리가 사라질 시간

            dist = ball.measure()
            if dist is None:
                misses += 1
                if misses >= config.MAX_MISSES:
                    fan.off()
                    pid.reset()
                    print("공 거리를 계속 못 읽어서 팬을 껐음. 센서 배선을 확인하세요.")
                    break
            else:
                misses = 0
                height = ball_height(dist)
                duty = args.hover + pid.update(target, height, period)
                fan.set(duty)

            now = monotonic() - t0
            if log and height is not None:
                p = pid.kp * (target - height)
                log.writerow([f"{now:.3f}", f"{target:.1f}", f"{height:.1f}", f"{fan.duty:.3f}",
                              f"{p:.4f}", f"{pid.integral:.4f}", f"{pid.d_term:.4f}"])
            if now - last_print >= 0.5:
                h = "  --" if height is None else f"{height:5.1f}"
                print(f"{now:6.1f}s  목표 {target:5.1f}cm  공 {h}cm  팬 {fan.duty * 100:5.1f}%")
                last_print = now

            next_tick += period
            delay = next_tick - monotonic()
            if delay > 0:
                sleep(delay)
            else:
                next_tick = monotonic()  # 늦었으면 주기를 다시 맞춤
    except KeyboardInterrupt:
        pass
    finally:
        fan.close()
        ball.close()
        if hand is not None:
            hand.close()
        if log_file:
            log_file.close()
        print("끝")


if __name__ == '__main__':
    main()
