from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class DevicePolicy:
    auto_on: bool
    on_delay: int
    off_delay: int
    safety_enabled: bool
    safety_timeout: int


@dataclass
class DeviceState:
    on: bool


@dataclass
class LightingState:
    main_on: bool
    low_on: bool


def is_night_low_light_time(current: str, start: str, end: str) -> bool:
    """Return True inside [start, end), including windows that cross midnight."""
    if start < end:
        return start <= current < end
    return current >= start or current < end


def automatic_lighting_start(
    lights: LightingState,
    policy: DevicePolicy,
    occupied_for: int,
    current: str,
    night_start: str,
    night_end: str,
) -> None:
    if not policy.auto_on or occupied_for < policy.on_delay:
        return

    if is_night_low_light_time(current, night_start, night_end):
        lights.low_on = True
    else:
        lights.main_on = True
        lights.low_on = True


def automatic_start(device: DeviceState, policy: DevicePolicy, occupied_for: int) -> None:
    if policy.auto_on and occupied_for >= policy.on_delay:
        device.on = True


def vacancy_shutdown_lighting(
    lights: LightingState,
    policy: DevicePolicy,
    return_after: int | None,
) -> None:
    if not (lights.main_on or lights.low_on):
        return
    if return_after is not None and return_after < policy.off_delay:
        return
    lights.main_on = False
    lights.low_on = False


def vacancy_shutdown(
    device: DeviceState,
    policy: DevicePolicy,
    return_after: int | None,
) -> None:
    if not device.on:
        return
    if return_after is not None and return_after < policy.off_delay:
        return
    device.on = False


def forgotten_lighting_safety(
    lights: LightingState,
    policy: DevicePolicy,
    return_after: int | None,
) -> None:
    if not (lights.main_on or lights.low_on) or not policy.safety_enabled:
        return
    if return_after is not None and return_after < policy.safety_timeout:
        return
    lights.main_on = False
    lights.low_on = False


def forgotten_device_safety(
    device: DeviceState,
    policy: DevicePolicy,
    return_after: int | None,
) -> None:
    if not device.on or not policy.safety_enabled:
        return
    if return_after is not None and return_after < policy.safety_timeout:
        return
    device.on = False


def startup_reconcile_lighting(
    lights: LightingState,
    startup_delay: int,
    occupied_after_startup: bool,
) -> None:
    del startup_delay
    if occupied_after_startup:
        return
    lights.main_on = False
    lights.low_on = False


def startup_reconcile(
    device: DeviceState,
    startup_delay: int,
    occupied_after_startup: bool,
) -> None:
    del startup_delay
    if occupied_after_startup:
        return
    device.on = False


def run_case(case_id: int) -> None:
    rng = random.Random(case_id)

    light_policy = DevicePolicy(
        auto_on=rng.choice([False, True]),
        on_delay=rng.choice([0, 5, 30, 60, 120]),
        off_delay=rng.choice([0, 30, 60, 90, 180, 600]),
        safety_enabled=rng.choice([False, True]),
        safety_timeout=rng.choice([60, 300, 900, 1800, 3600, 7200]),
    )
    fan_policy = DevicePolicy(
        auto_on=rng.choice([False, True]),
        on_delay=rng.choice([0, 30, 60, 120, 300]),
        off_delay=rng.choice([0, 120, 300, 420, 600, 1200]),
        safety_enabled=rng.choice([False, True]),
        safety_timeout=rng.choice([60, 600, 1800, 3600, 7200, 14400]),
    )

    night_start = rng.choice(["21:00:00", "23:00:00", "23:30:00"])
    night_end = rng.choice(["06:00:00", "08:00:00", "09:00:00"])
    current = rng.choice([
        "00:00:00",
        "05:59:59",
        "07:59:59",
        "08:00:00",
        "12:00:00",
        "22:59:59",
        "23:00:00",
        "23:59:59",
    ])

    scenario = rng.choice(["occupied_cycle", "manual_while_vacant", "startup"])
    return_after = rng.choice([None, 0, 15, 45, 90, 300, 900, 3600])

    if scenario == "occupied_cycle":
        occupied_for = rng.choice([0, 10, 30, 60, 180, 600])
        initial_main = rng.choice([False, True])
        initial_low = rng.choice([False, True])
        initial_fan = rng.choice([False, True])

        lights = LightingState(initial_main, initial_low)
        fan = DeviceState(initial_fan)

        automatic_lighting_start(
            lights,
            light_policy,
            occupied_for,
            current,
            night_start,
            night_end,
        )
        automatic_start(fan, fan_policy, occupied_for)

        if light_policy.auto_on and occupied_for >= light_policy.on_delay:
            if is_night_low_light_time(current, night_start, night_end):
                assert lights.low_on is True
                assert lights.main_on is initial_main
            else:
                assert lights.main_on is True
                assert lights.low_on is True
        else:
            assert lights.main_on is initial_main
            assert lights.low_on is initial_low

        expected_fan_after_start = initial_fan or (
            fan_policy.auto_on and occupied_for >= fan_policy.on_delay
        )
        assert fan.on is expected_fan_after_start

        lighting_before = (lights.main_on, lights.low_on)
        fan_before = fan.on

        vacancy_shutdown_lighting(lights, light_policy, return_after)
        vacancy_shutdown(fan, fan_policy, return_after)

        if any(lighting_before):
            if return_after is not None and return_after < light_policy.off_delay:
                assert (lights.main_on, lights.low_on) == lighting_before
            else:
                assert lights.main_on is False
                assert lights.low_on is False

        if fan_before:
            if return_after is not None and return_after < fan_policy.off_delay:
                assert fan.on is True
            else:
                assert fan.on is False

    elif scenario == "manual_while_vacant":
        lights = LightingState(
            main_on=rng.choice([False, True]),
            low_on=rng.choice([False, True]),
        )
        fan = DeviceState(rng.choice([False, True]))

        lighting_before = (lights.main_on, lights.low_on)
        fan_before = fan.on

        forgotten_lighting_safety(lights, light_policy, return_after)
        forgotten_device_safety(fan, fan_policy, return_after)

        if any(lighting_before):
            if not light_policy.safety_enabled:
                assert (lights.main_on, lights.low_on) == lighting_before
            elif return_after is not None and return_after < light_policy.safety_timeout:
                assert (lights.main_on, lights.low_on) == lighting_before
            else:
                assert lights.main_on is False
                assert lights.low_on is False

        if fan_before:
            if not fan_policy.safety_enabled:
                assert fan.on is True
            elif return_after is not None and return_after < fan_policy.safety_timeout:
                assert fan.on is True
            else:
                assert fan.on is False

    else:
        lights = LightingState(
            main_on=rng.choice([False, True]),
            low_on=rng.choice([False, True]),
        )
        fan = DeviceState(rng.choice([False, True]))
        occupied_after_startup = rng.choice([False, True])
        startup_delay = rng.choice([0, 15, 30, 60, 120])

        lighting_before = (lights.main_on, lights.low_on)
        fan_before = fan.on

        startup_reconcile_lighting(lights, startup_delay, occupied_after_startup)
        startup_reconcile(fan, startup_delay, occupied_after_startup)

        if occupied_after_startup:
            assert (lights.main_on, lights.low_on) == lighting_before
            assert fan.on is fan_before
        else:
            assert lights.main_on is False
            assert lights.low_on is False
            assert fan.on is False


def boundary_tests() -> None:
    # Default requested overnight window: 23:00 -> 08:00.
    assert is_night_low_light_time("22:59:59", "23:00:00", "08:00:00") is False
    assert is_night_low_light_time("23:00:00", "23:00:00", "08:00:00") is True
    assert is_night_low_light_time("00:00:00", "23:00:00", "08:00:00") is True
    assert is_night_low_light_time("07:59:59", "23:00:00", "08:00:00") is True
    assert is_night_low_light_time("08:00:00", "23:00:00", "08:00:00") is False

    # Also verify a same-day window for reusable logic.
    assert is_night_low_light_time("20:00:00", "18:00:00", "22:00:00") is True
    assert is_night_low_light_time("22:00:00", "18:00:00", "22:00:00") is False


def main() -> None:
    boundary_tests()
    for case_id in range(1, 101):
        run_case(case_id)

    print("BATHROOM LOGIC TEST PASSED: 100/100 deterministic scenarios + night boundaries")


if __name__ == "__main__":
    main()
