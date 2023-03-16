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
    """Tests that general sensor can assign a value"""
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
    expected = np.array([0, 0, 1, 20])
    creation = ColorSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(expected)
    assert np.array_equal(creation.value, expected)


def test_color_sensor_error():
    """Tests if error is raised for value of wrong size"""
    expectedError = RGBSensorValueError
    creation = ColorSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    with raises(expectedError):
        creation._update_value(np.array([0,1]))


def test_distance_sensor():
    """Tests if the distance sensor value assigning and creation works"""
    creation = DistanceSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(1)
    assert creation.value == 1


def test_distance_sensor_none():
    """tests that distance sensor can be assigned nne"""
    creation = DistanceSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(None)
    assert creation.value is None


def test_distance_sensor_error():
    """test that distance sensor raises error"""
    creation = DistanceSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    with raises(DistanceValueError):
        creation._update_value("error")


def test_force_sensor():
    """tests that force sensor can be updated and created"""
    creation = ForceSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))
    creation._update_value(1)
    assert creation.value == 1


def test_gyro_sensor():
    """test gyro sensor can be created and updated"""
    creation = GyroSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))

    expected = np.array([0, 0, 0])
    creation._update_value(expected)
    assert np.array_equal(expected, creation.value)


def test_gyro_sensor_error():
    """tests gyro sensor can't be assigned incorrect value"""
    expected = GyroValueError
    creation = GyroSensor("test", direction=np.array([0, 0, 1]), position=np.array([0, 0, 1]))

    error_val = np.array([0,])
    with raises(expected):
        creation._update_value(error_val)
