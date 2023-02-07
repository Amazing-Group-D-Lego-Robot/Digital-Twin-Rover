import time
from copy import deepcopy

import pytest

from twin.twin_system import TwinSystem
from twin.twin_environment import TwinEnvironment
from twin.twin_model import TwinModel


def test_prediction_format():
    twin_system = TwinSystem(True)

    out = twin_system.predict_next()

    assert len(out) == 2, "Two outputs expected from TwinSystem.predict_next()"

    assert isinstance(out[0], list), "First returned value of TwinSystem.predict_next() should be a list"
    assert isinstance(out[1], TwinEnvironment), "Second returned value of TwinSystem.predict_next() should be the " \
                                                "TwinEnvironment"

    assert len(out[0]) == 1, "The default value of TwinSystem.predict_next() should only return one prediction"
    assert isinstance(out[0][0], TwinModel), "The prediction list should contain TwinModel elements"

    savestate = deepcopy(twin_system)
    out = twin_system.predict_next(n=10)

    assert twin_system.worldstate.twin.x_pos == savestate.worldstate.twin.x_pos, "Predictions should not change the " \
                                                                                 "state of the model"

    assert len(out[0]) == 10, "TwinSystem.predict_next(n=10) should return ten predictions"


def test_default_model_update():
    twin_system = TwinSystem(True)

    twin_system.worldstate.twin.x_acc = 0.1
    twin_system.worldstate.twin.y_acc = 0.2
    twin_system.worldstate.twin.z_acc = 0.3

    twin_system.update()
    time.sleep(1)
    twin_system.update()

    assert twin_system.worldstate.twin.x_vel == pytest.approx(0.1, abs=0.01)
    assert twin_system.worldstate.twin.y_vel == pytest.approx(0.2, abs=0.01)
    assert twin_system.worldstate.twin.z_vel == pytest.approx(0.3, abs=0.01)

    assert twin_system.worldstate.twin.x_pos == pytest.approx(0.1, abs=0.01)
    assert twin_system.worldstate.twin.y_pos == pytest.approx(0.2, abs=0.01)
    assert twin_system.worldstate.twin.z_pos == pytest.approx(0.3, abs=0.01)

    time.sleep(1)
    twin_system.update()

    assert twin_system.worldstate.twin.x_vel == pytest.approx(0.2, abs=0.01)
    assert twin_system.worldstate.twin.y_vel == pytest.approx(0.4, abs=0.01)
    assert twin_system.worldstate.twin.z_vel == pytest.approx(0.6, abs=0.01)

    assert twin_system.worldstate.twin.x_pos == pytest.approx(0.3, abs=0.01)
    assert twin_system.worldstate.twin.y_pos == pytest.approx(0.6, abs=0.01)
    assert twin_system.worldstate.twin.z_pos == pytest.approx(0.9, abs=0.01)
