from __future__ import annotations

from dataclasses import dataclass
import random


@dataclass
class BathroomModel:
    light_on: bool
    fan_on: bool
    light_owned: bool = False
    fan_owned: bool = False

    def occupied(self) -> None:
        # Reconcile stale ownership only when the whole class is OFF.
        if self.light_owned and not self.light_on:
            self.light_owned = False
        if self.fan_owned and not self.fan_on:
            self.fan_owned = False

        # Claim only devices/classes that were OFF before this occupancy cycle.
        if not self.light_owned and not self.light_on:
            self.light_on = True
            self.light_owned = True

        if not self.fan_owned and not self.fan_on:
            self.fan_on = True
            self.fan_owned = True

    def vacancy_completed(self) -> None:
        if self.light_owned:
            self.light_on = False
            self.light_owned = False

        if self.fan_owned:
            self.fan_on = False
            self.fan_owned = False

    def vacancy_interrupted_by_occupancy(self) -> None:
        # mode: restart cancels the pending shutdown run.
        self.occupied()


def run_case(case_id: int) -> None:
    rng = random.Random(case_id)

    initial_manual_light = rng.choice([False, True])
    initial_manual_fan = rng.choice([False, True])
    occupancy_returns = rng.choice([False, True])

    model = BathroomModel(
        light_on=initial_manual_light,
        fan_on=initial_manual_fan,
    )

    model.occupied()

    # Ownership must never be claimed over a pre-existing manual state.
    if initial_manual_light:
        assert model.light_on is True
        assert model.light_owned is False
    else:
        assert model.light_on is True
        assert model.light_owned is True

    if initial_manual_fan:
        assert model.fan_on is True
        assert model.fan_owned is False
    else:
        assert model.fan_on is True
        assert model.fan_owned is True

    if occupancy_returns:
        model.vacancy_interrupted_by_occupancy()

        # Returning occupancy must not shut down automation-owned devices.
        assert model.light_on is True
        assert model.fan_on is True

    model.vacancy_completed()

    # Pre-existing manual states must survive an automation vacancy cycle.
    if initial_manual_light:
        assert model.light_on is True
    else:
        assert model.light_on is False

    if initial_manual_fan:
        assert model.fan_on is True
    else:
        assert model.fan_on is False

    # Ownership is released only for classes the automation owned.
    assert model.light_owned is False
    assert model.fan_owned is False


def main() -> None:
    for case_id in range(1, 101):
        run_case(case_id)

    print("BATHROOM LOGIC TEST PASSED: 100/100 deterministic scenarios")


if __name__ == "__main__":
    main()
