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


def automatic_start(device: DeviceState, policy: DevicePolicy, occupied_for: int) -> None:
    if policy.auto_on and occupied_for >= policy.on_delay:
        device.on = True


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


def startup_reconcile(
    device: DeviceState,
    policy: DevicePolicy,
    startup_delay: int,
    occupied_after_startup: bool,
) -> None:
    del startup_delay  # Timing is represented by entering this function after the delay.
    if occupied_after_startup:
        return
    if device.on:
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

    scenario = rng.choice(["occupied_cycle", "manual_while_vacant", "startup"])
    return_after = rng.choice([None, 0, 15, 45, 90, 300, 900, 3600])

    if scenario == "occupied_cycle":
        occupied_for = rng.choice([0, 10, 30, 60, 180, 600])
        initial_light = rng.choice([False, True])
        initial_fan = rng.choice([False, True])

        light = DeviceState(initial_light)
        fan = DeviceState(initial_fan)

        automatic_start(light, light_policy, occupied_for)
        automatic_start(fan, fan_policy, occupied_for)

        expected_light_after_start = initial_light or (
            light_policy.auto_on and occupied_for >= light_policy.on_delay
        )
        expected_fan_after_start = initial_fan or (
            fan_policy.auto_on and occupied_for >= fan_policy.on_delay
        )

        assert light.on is expected_light_after_start
        assert fan.on is expected_fan_after_start

        light_before = light.on
        fan_before = fan.on

        vacancy_shutdown(light, light_policy, return_after)
        vacancy_shutdown(fan, fan_policy, return_after)

        if light_before:
            if return_after is not None and return_after < light_policy.off_delay:
                assert light.on is True
            else:
                assert light.on is False

        if fan_before:
            if return_after is not None and return_after < fan_policy.off_delay:
                assert fan.on is True
            else:
                assert fan.on is False

    elif scenario == "manual_while_vacant":
        light = DeviceState(rng.choice([False, True]))
        fan = DeviceState(rng.choice([False, True]))

        light_before = light.on
        fan_before = fan.on

        forgotten_device_safety(light, light_policy, return_after)
        forgotten_device_safety(fan, fan_policy, return_after)

        if light_before:
            if not light_policy.safety_enabled:
                assert light.on is True
            elif return_after is not None and return_after < light_policy.safety_timeout:
                assert light.on is True
            else:
                assert light.on is False

        if fan_before:
            if not fan_policy.safety_enabled:
                assert fan.on is True
            elif return_after is not None and return_after < fan_policy.safety_timeout:
                assert fan.on is True
            else:
                assert fan.on is False

    else:
        light = DeviceState(rng.choice([False, True]))
        fan = DeviceState(rng.choice([False, True]))
        occupied_after_startup = rng.choice([False, True])
        startup_delay = rng.choice([0, 15, 30, 60, 120])

        light_before = light.on
        fan_before = fan.on

        startup_reconcile(light, light_policy, startup_delay, occupied_after_startup)
        startup_reconcile(fan, fan_policy, startup_delay, occupied_after_startup)

        if occupied_after_startup:
            assert light.on is light_before
            assert fan.on is fan_before
        else:
            assert light.on is False
            assert fan.on is False


def main() -> None:
    for case_id in range(1, 101):
        run_case(case_id)

    print("BATHROOM LOGIC TEST PASSED: 100/100 deterministic no-helper scenarios")


if __name__ == "__main__":
    main()
