import pytest
from types import SimpleNamespace
from custom_components.solar_split.sensor import SolarSplitSensor


# Mock State object like Home Assistant's core.State
class MockState:
    def __init__(self, state, unit="W"):
        self.state = str(state)
        self.attributes = {"unit_of_measurement": unit}


# Mock hass object with .states.get()
class MockHass:
    def __init__(self, states_dict):
        self._states = states_dict

    @property
    def states(self):
        return self

    def get(self, entity_id):
        return self._states.get(entity_id)


def test_solar_used_only():
    hass = MockHass(
        {
            "sensor.solar": MockState(3000),
            "sensor.device_1": MockState(2000),
        }
    )

    sensor = SolarSplitSensor(
        name="Device 1 Solar",
        device_sensor_id="sensor.device_1",
        solar_sensor_id="sensor.solar",
        priority_index=0,
        all_devices=[hass.get("sensor.device_1")],
        is_grid=False,
    )
    sensor.hass = hass

    assert sensor.state == 2000  # All from solar


def test_grid_used_only():
    hass = MockHass(
        {
            "sensor.solar": MockState(0),
            "sensor.device_1": MockState(1500),
        }
    )

    sensor = SolarSplitSensor(
        name="Device 1 Grid",
        device_sensor_id="sensor.device_1",
        solar_sensor_id="sensor.solar",
        priority_index=0,
        all_devices=[hass.get("sensor.device_1")],
        is_grid=True,
    )
    sensor.hass = hass

    assert sensor.state == 1500  # All from grid


def test_partial_solar_partial_grid():
    hass = MockHass(
        {
            "sensor.solar": MockState(1000),
            "sensor.device_1": MockState(1500),
        }
    )

    solar_sensor = SolarSplitSensor(
        name="Device 1 Solar",
        device_sensor_id="sensor.device_1",
        solar_sensor_id="sensor.solar",
        priority_index=0,
        all_devices=[hass.get("sensor.device_1")],
        is_grid=False,
    )
    grid_sensor = SolarSplitSensor(
        name="Device 1 Grid",
        device_sensor_id="sensor.device_1",
        solar_sensor_id="sensor.solar",
        priority_index=0,
        all_devices=[hass.get("sensor.device_1")],
        is_grid=True,
    )

    solar_sensor.hass = hass
    grid_sensor.hass = hass
    assert solar_sensor.state == 1000
    assert grid_sensor.state == 500
