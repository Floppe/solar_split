from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up from configuration.yaml (if supported)."""
    _LOGGER.debug("async_setup called")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.debug("async_setup_entry called for %s", entry.entry_id)
    """Set up Solar Split from a config entry."""

    def get(key):
        return entry.options.get(key) or entry.data.get(key) or ""

    # Retrieve updated config values
    name = get("name")
    solar_sensor = get("solar_sensor")
    device_1 = get("device_1")
    device_2 = get("device_2")
    device_3 = get("device_3")
    device_4 = get("device_4")
    device_5 = get("device_5")
    device_6 = get("device_6")
    device_7 = get("device_7")

    # You can store these in hass.data if needed
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "name": name,
        "solar_sensor": solar_sensor,
        "devices": [
            d for d in [device_1, device_2, device_3, device_4, device_5, device_6, device_7] if d
        ],
    }

    # Forward to platform(s) like sensor.py
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
