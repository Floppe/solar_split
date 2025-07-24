from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class SolarSplitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Solar Split", data=user_input)

        sensors = [
            state.entity_id for state in self.hass.states.async_all("sensor")
            if state.attributes.get("unit_of_measurement") in ("W", "kW")
        ]
        sensor_options = sorted(sensors)

        schema = vol.Schema({
            vol.Required("solar_sensor"): vol.In(sensor_options),
            vol.Optional("device_1"): vol.In(sensor_options),
            vol.Optional("device_2"): vol.In(sensor_options),
            vol.Optional("device_3"): vol.In(sensor_options),
            vol.Optional("device_4"): vol.In(sensor_options),
            vol.Optional("device_5"): vol.In(sensor_options),
            vol.Optional("device_6"): vol.In(sensor_options),
            vol.Optional("device_7"): vol.In(sensor_options),
        })

        return self.async_show_form(step_id="user", data_schema=schema)
