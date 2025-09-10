import voluptuous as vol
import logging
from homeassistant.core import callback
from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigFlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class SolarSplitConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        _LOGGER.debug("async_step_user called with user_input: %s", user_input)

        errors = {}

        if user_input is not None:
            # You can add validation here if needed
            _LOGGER.debug("Options submitted: %s", user_input)
            return self.async_create_entry(title="Solar Split", data=user_input)

        sensors = [
            state.entity_id for state in self.hass.states.async_all("sensor")
            if state.attributes.get("unit_of_measurement") in ("W", "kW")
        ]
        sensor_options = sorted(sensors)

        data_schema = vol.Schema({
            vol.Required("name", default="Solar split"): str,
            vol.Required("solar_sensor"): vol.In(sensor_options),
            vol.Required("device_1"): vol.In(sensor_options),
            vol.Optional("device_2"): vol.In([""] + sensor_options),
            vol.Optional("device_3"): vol.In([""] + sensor_options),
            vol.Optional("device_4"): vol.In([""] + sensor_options),
            vol.Optional("device_5"): vol.In([""] + sensor_options),
            vol.Optional("device_6"): vol.In([""] + sensor_options),
            vol.Optional("device_7"): vol.In([""] + sensor_options),
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SolarSplitOptionsFlow(config_entry)

class SolarSplitOptionsFlow(OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_set_entry(self, config_entry):
        """Called by Home Assistant 2025.12+ to set config_entry."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input: None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title="Solar Split", data=user_input)

        sensors = [
            state.entity_id for state in self.hass.states.async_all("sensor")
            if state.attributes.get("unit_of_measurement") in ("W", "kW")
        ]
        sensor_options = sorted(sensors)

        def get(key):
            if self.config_entry is None:
                _LOGGER.debug("config_entry is none, cannot get key: %s", key)
                return ""
            return self.config_entry.options.get(key, self.config_entry.data.get(key, ""))

        data_schema = vol.Schema({
            vol.Required("name", default=get("name")): str,
            vol.Required("solar_sensor", default=get("solar_sensor")): vol.In(sensor_options),
            vol.Required("device_1", default=get("device_1")): vol.In(sensor_options),
            vol.Optional("device_2", default=get("device_2")): vol.In([""] + sensor_options),
            vol.Optional("device_3", default=get("device_3")): vol.In([""] + sensor_options),
            vol.Optional("device_4", default=get("device_4")): vol.In([""] + sensor_options),
            vol.Optional("device_5", default=get("device_5")): vol.In([""] + sensor_options),
            vol.Optional("device_6", default=get("device_6")): vol.In([""] + sensor_options),
            vol.Optional("device_7", default=get("device_7")): vol.In([""] + sensor_options),
        })

        return self.async_show_form(step_id="init", data_schema=data_schema)
