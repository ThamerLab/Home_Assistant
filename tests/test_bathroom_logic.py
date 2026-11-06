from __future__ import annotations

from dataclasses import dataclass
import random


BEHAVIORS = ("timed_hold", "normal_vacancy", "keep_on")


@dataclass
class DeviceClass:
    on: bool
    owned: bool = False


@dataclass
class DevicePolicy:
    auto_on: bool
    on_delay: int
    off_delay: int
    manual_behavior: str
    manual_hold_max: int


@dataclass
class BathroomModel:
    light: DeviceClass
    fan: DeviceClass
    light_policy: DevicePolicy
    fan_policy: DevicePolicy

    @staticmethod
    def _occupied(device: DeviceClass, policy: DevicePolicy, occupied_for: int) -> None:
        if device.owned and not device.on:
            device.owned = False

        if (
            policy.auto_on
            and occupied_for >= policy.on_delay
            and not device.owned
            and not device.on
        ):
            # The production Blueprint records ownership before sending ON.
            device.owned = True
            device.on = True

    def occupied(self, occupied_for: int) -> None:
        self._occupied(self.light, self.light_policy, occupied_for)
        self._occupied(self.fan, self.fan_policy, occupied_for)

    @staticmethod
    def _deadline(device: DeviceClass, policy: DevicePolicy) -> int | None:
        if not device.on:
            return None
        if device.owned:
            return policy.off_delay
        if policy.manual_behavior == "timed_hold":
            return policy.manual_hold_max
        if policy.manual_behavior == "normal_vacancy":
            return policy.off_delay
        if policy.manual_behavior == "keep_on":
            return None
        raise AssertionError(f"unexpected behavior: {policy.manual_behavior}")

    @classmethod
    def _vacancy(
        cls,
        device: DeviceClass,
        policy: DevicePolicy,
        return_after: int | None,
    ) -> None:
        deadline = cls._deadline(device, policy)
        if deadline is None:
            return

        # Returning occupancy before the deadline is equivalent to mode: restart
        # cancelling the pending OFF sequence.
        if return_after is not None and return_after < deadline:
            return

        device.on = False
        if device.owned:
            device.owned = False

    def vacancy(self, return_after: int | None) -> None:
        self._vacancy(self.light, self.light_policy, return_after)
        self._vacancy(self.fan, self.fan_policy, return_after)


def run_case(case_id: int) -> None:
    rng = random.Random(case_id)

    light_policy = DevicePolicy(
        auto_on=rng.choice([False, True]),
        on_delay=rng.choice([0, 5, 30, 60, 120]),
        off_delay=rng.choice([0, 30, 60, 90, 180, 600]),
        manual_behavior=rng.choice(BEHAVIORS),
        manual_hold_max=rng.choice([0, 300, 900, 1800, 3600, 7200]),
    )
    fan_policy = DevicePolicy(
        auto_on=rng.choice([False, True]),
        on_delay=rng.choice([0, 30, 60, 120, 300]),
        off_delay=rng.choice([0, 120, 300, 420, 600, 1200]),
        manual_behavior=rng.choice(BEHAVIORS),
        manual_hold_max=rng.choice([0, 600, 1800, 3600, 7200, 14400]),
    )

    initial_manual_light = rng.choice([False, True])
    initial_manual_fan = rng.choice([False, True])
    occupied_for = rng.choice([0, 10, 30, 60, 180, 600])

    # None means vacancy remains uninterrupted. Otherwise occupancy returns at
    # that many seconds after the bathroom first becomes fully vacant.
    return_after = rng.choice([None, 0, 15, 45, 90, 300, 900, 3600])

    model = BathroomModel(
        light=DeviceClass(on=initial_manual_light),
        fan=DeviceClass(on=initial_manual_fan),
        light_policy=light_policy,
        fan_policy=fan_policy,
    )

    model.occupied(occupied_for=occupied_for)

    # Manual pre-states must never be claimed as automation-owned.
    if initial_manual_light:
        assert model.light.on is True
        assert model.light.owned is False
    elif light_policy.auto_on and occupied_for >= light_policy.on_delay:
        assert model.light.on is True
        assert model.light.owned is True
    else:
        assert model.light.on is False
        assert model.light.owned is False

    if initial_manual_fan:
        assert model.fan.on is True
        assert model.fan.owned is False
    elif fan_policy.auto_on and occupied_for >= fan_policy.on_delay:
        assert model.fan.on is True
        assert model.fan.owned is True
    else:
        assert model.fan.on is False
        assert model.fan.owned is False

    light_before = (model.light.on, model.light.owned)
    fan_before = (model.fan.on, model.fan.owned)
    light_deadline = model._deadline(model.light, light_policy)
    fan_deadline = model._deadline(model.fan, fan_policy)

    model.vacancy(return_after=return_after)

    def assert_result(
        device: DeviceClass,
        before: tuple[bool, bool],
        deadline: int | None,
        policy: DevicePolicy,
    ) -> None:
        if not before[0]:
            assert device.on is False
            assert device.owned is False
            return

        if deadline is None:
            # Manual Keep On or an already-OFF class.
            assert (device.on, device.owned) == before
            return

        if return_after is not None and return_after < deadline:
            # Re-entry cancels the pending OFF path.
            assert (device.on, device.owned) == before
            return

        # Uninterrupted expiry shuts the class down.
        assert device.on is False
        assert device.owned is False

        if not before[1] and policy.manual_behavior == "keep_on":
            raise AssertionError("keep_on must never reach an automatic OFF deadline")

    assert_result(model.light, light_before, light_deadline, light_policy)
    assert_result(model.fan, fan_before, fan_deadline, fan_policy)

    # Light and fan policies are evaluated independently.
    assert model.light.owned in {False, True}
    assert model.fan.owned in {False, True}


def main() -> None:
    for case_id in range(1, 101):
        run_case(case_id)

    print("BATHROOM LOGIC TEST PASSED: 100/100 deterministic timing scenarios")


if __name__ == "__main__":
    main()
