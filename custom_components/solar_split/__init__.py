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
    """Set up Solar Split from a config entry."""
    _LOGGER.debug("async_setup_entry called for %s", entry.entry_id)

    def get(key):
        return entry.options.get(key) or entry.data.get(key) or ""

    # collect devices, filtering out empty strings
    devices = [get(f"device_{i}") for i in range(1, 8)]
    devices = [d for d in devices if d]

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "name": get("name"),
        "solar_sensor": get("solar_sensor"),
        "devices": devices
    }

    # forward to platform(s) like sensor.py
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    # safely register reload listener only once
    if not entry.update_listeners:
        entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok

async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Safely reload config entry without infinite loop."""
    _LOGGER.debug("Manually reloading entry: %s", entry.entry_id)
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
