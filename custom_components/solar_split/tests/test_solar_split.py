import pytest
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntryState
from homeassistant.helpers.entity_component import async_update_entity
from custom_components.solar_split.const import DOMAIN

from homeassistant.setup import async_setup_component

MOCK_CONFIG = {
    "name": "Test Split",
    "solar_sensor": "sensor.solar",
    "device_1": "sensor.device_1",
    "device_2": "sensor.device_2"
}

@pytest.fixture
async def setup_integration(hass: HomeAssistant):
    # Mock sensor states
    hass.states.async_set("sensor.solar", "500", {"unit_of_measurement": "W"})
    hass.states.async_set("sensor.device_1", "300", {"unit_of_measurement": "W"})
    hass.states.async_set("sensor.device_2", "250", {"unit_of_measurement": "W"})

    # Setup the integration
    assert await async_setup_component(hass, "sensor", {})

    entry = hass.config_entries.async_create(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    hass.config_entries._entries.append(entry)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    yield entry

    await hass.config_entries.async_unload(entry.entry_id)


async def test_entities_created(hass: HomeAssistant, setup_integration):
    """Test that sensors are created and provide expected state."""
    solar_entity_id = "sensor.device_1_solar"
    grid_entity_id = "sensor.device_1_grid"

    await async_update_entity(hass, solar_entity_id)
    await async_update_entity(hass, grid_entity_id)

    solar_state = hass.states.get(solar_entity_id)
    grid_state = hass.states.get(grid_entity_id)

    assert solar_state is not None
    assert grid_state is not None

    assert float(solar_state.state) > 0
    assert float(grid_state.state) >= 0


async def test_reload_entry(hass: HomeAssistant, setup_integration):
    """Test that the integration reloads without error."""
    entry = setup_integration

    assert entry.state == ConfigEntryState.LOADED

    await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()

    assert entry.state == ConfigEntryState.LOADED
