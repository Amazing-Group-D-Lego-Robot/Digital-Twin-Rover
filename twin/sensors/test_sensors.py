import numpy as np

from twin.sensors.sensor import Sensor
from twin.sensors.acceleration_sensor import AccelerationSensor
from twin.sensors.color_sensor import ColorSensor
from twin.sensors.distance_sensor import DistanceSensor
from twin.sensors.force_sensor import ForceSensor
from twin.sensors.gyro_sensor import GyroSensor

from twin.sensors.errors.sensor_errors import *

from pytest import raises


def test_general_sensor():
    creation = Sensor("yaw")
    creation._update_value(2)
    assert creation.value == 2


def test_acceleration_sensor():
    """Test for acceleration along same axis agent faces"""
    expected = np.array([1, 1, 1])
    creation = AccelerationSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(expected)
    assert np.array_equal(creation.value, expected)


def test_acceleration_error():
    """Test for acceleration if wrong size numpy array is entered"""
    expected = AccelerationValueError
    with raises(AccelerationValueError):
        expected = np.array([1, 11])
        creation = AccelerationSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
        creation._update_value(expected)


def test_colour_sensor():
    """Tests if value updating is correct"""
    expected = np.arrya([0, 0, 1, 20])
    creation = ColorSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(expected)
    assert creation.value == expected


def test_color_sensor_error():
    """Tests if error is raised for value of wrong size"""
    expectedError = RGBSensorValueError
    creation = ColorSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    with raises(expectedError):
        creation._update_value([1, 2])


def test_distance_sensor():
    creation = DistanceSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(1)
    assert creation.value == 1


def test_distance_sensor_none():
    creation = DistanceSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(None)
    assert creation.value is None


def test_distance_sensor_error():
    creation = DistanceSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    with raises(DistanceValueError):
        creation._update_value("error")


def test_force_sensor():
    creation = ForceSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(1)
    assert creation.value == 1


def test_gyro_sensor():
    creation = GyroSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))

    expected = np.array([0, 0, 0])
    creation._update_value(expected)
    assert np.array_equal(expected, creation.value)


def test_gyro_sensor_error():
    expected = GyroValueError
    creation = GyroSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))

    error_val = np.array([0,])
    with raises(expected):
        creation._update_value(error_val)
