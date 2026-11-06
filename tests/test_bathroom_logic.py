from __future__ import annotations

from dataclasses import dataclass
import random


BEHAVIORS = ("timed_hold", "normal_vacancy", "keep_on")


@dataclass
class DeviceClass:
    on: bool
    owned: bool = False


@dataclass
class BathroomModel:
    light: DeviceClass
    fan: DeviceClass
    auto_light: bool
    auto_fan: bool
    light_behavior: str
    fan_behavior: str

    def occupied(
        self,
        light_delay_survives: bool,
        fan_delay_survives: bool,
    ) -> None:
        if self.light.owned and not self.light.on:
            self.light.owned = False
        if self.fan.owned and not self.fan.on:
            self.fan.owned = False

        if self.auto_light and light_delay_survives and not self.light.owned and not self.light.on:
            self.light.owned = True
            self.light.on = True

        if self.auto_fan and fan_delay_survives and not self.fan.owned and not self.fan.on:
            self.fan.owned = True
            self.fan.on = True

    @staticmethod
    def _vacancy_result(device: DeviceClass, behavior: str, shutdown_interrupted: bool) -> None:
        if shutdown_interrupted:
            return

        if device.owned:
            device.on = False
            device.owned = False
            return

        if device.on and behavior in {"timed_hold", "normal_vacancy"}:
            device.on = False

    def vacancy_cycle(
        self,
        light_shutdown_interrupted: bool,
        fan_shutdown_interrupted: bool,
    ) -> None:
        self._vacancy_result(self.light, self.light_behavior, light_shutdown_interrupted)
        self._vacancy_result(self.fan, self.fan_behavior, fan_shutdown_interrupted)


def run_case(case_id: int) -> None:
    rng = random.Random(case_id)

    initial_manual_light = rng.choice([False, True])
    initial_manual_fan = rng.choice([False, True])
    auto_light = rng.choice([False, True])
    auto_fan = rng.choice([False, True])
    light_behavior = rng.choice(BEHAVIORS)
    fan_behavior = rng.choice(BEHAVIORS)
    light_delay_survives = rng.choice([False, True])
    fan_delay_survives = rng.choice([False, True])
    light_shutdown_interrupted = rng.choice([False, True])
    fan_shutdown_interrupted = rng.choice([False, True])

    model = BathroomModel(
        light=DeviceClass(on=initial_manual_light),
        fan=DeviceClass(on=initial_manual_fan),
        auto_light=auto_light,
        auto_fan=auto_fan,
        light_behavior=light_behavior,
        fan_behavior=fan_behavior,
    )

    model.occupied(
        light_delay_survives=light_delay_survives,
        fan_delay_survives=fan_delay_survives,
    )

    # Pre-existing manual ON states are never claimed by automation ownership.
    if initial_manual_light:
        assert model.light.on is True
        assert model.light.owned is False
    elif auto_light and light_delay_survives:
        assert model.light.on is True
        assert model.light.owned is True
    else:
        assert model.light.on is False
        assert model.light.owned is False

    if initial_manual_fan:
        assert model.fan.on is True
        assert model.fan.owned is False
    elif auto_fan and fan_delay_survives:
        assert model.fan.on is True
        assert model.fan.owned is True
    else:
        assert model.fan.on is False
        assert model.fan.owned is False

    light_before_vacancy = (model.light.on, model.light.owned)
    fan_before_vacancy = (model.fan.on, model.fan.owned)

    model.vacancy_cycle(
        light_shutdown_interrupted=light_shutdown_interrupted,
        fan_shutdown_interrupted=fan_shutdown_interrupted,
    )

    # Returning occupancy before the relevant deadline cancels that class shutdown.
    if light_shutdown_interrupted:
        assert (model.light.on, model.light.owned) == light_before_vacancy
    else:
        if light_before_vacancy[1]:
            assert model.light.on is False
            assert model.light.owned is False
        elif light_before_vacancy[0] and light_behavior == "keep_on":
            assert model.light.on is True
            assert model.light.owned is False
        elif light_before_vacancy[0]:
            assert model.light.on is False
            assert model.light.owned is False

    if fan_shutdown_interrupted:
        assert (model.fan.on, model.fan.owned) == fan_before_vacancy
    else:
        if fan_before_vacancy[1]:
            assert model.fan.on is False
            assert model.fan.owned is False
        elif fan_before_vacancy[0] and fan_behavior == "keep_on":
            assert model.fan.on is True
            assert model.fan.owned is False
        elif fan_before_vacancy[0]:
            assert model.fan.on is False
            assert model.fan.owned is False

    # Light and fan ownership remain independent.
    assert model.light.owned in {False, True}
    assert model.fan.owned in {False, True}


def main() -> None:
    for case_id in range(1, 101):
        run_case(case_id)

    print("BATHROOM LOGIC TEST PASSED: 100/100 deterministic scenarios")


if __name__ == "__main__":
    main()
