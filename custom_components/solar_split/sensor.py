from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfPower
from homeassistant.helpers.event import async_track_state_change_event

async def async_setup_entry(hass, config_entry, async_add_entities):
    data = {**config_entry.data, **config_entry.options}
    solar_sensor = data["solar_sensor"]
    device_ids = [data.get(f"device_{i}") for i in range(1, 8)]
    device_ids = [d for d in device_ids if d]

    if not device_ids:
        _LOGGER.warning("No devices configured for solar_split.")
        return

    entities = []
    all_entities = [hass.states.get(sensor_id) for sensor_id in device_ids]

    for i, sensor_id in enumerate(device_ids):
        name = sensor_id.split(".")[-1].replace("_", " ").title()
        entities.append(SolarSplitSensor(f"{name} Solar", sensor_id, solar_sensor, i, all_entities, is_grid=False))
        entities.append(SolarSplitSensor(f"{name} Grid", sensor_id, solar_sensor, i, all_entities, is_grid=True))

    async_add_entities(entities, update_before_add=True)

class SolarSplitSensor(SensorEntity):
    def __init__(self, name, device_sensor_id, solar_sensor_id, priority_index, all_devices, is_grid):
        self._name = name
        self._device_sensor_id = device_sensor_id
        self._solar_sensor_id = solar_sensor_id
        self._priority_index = priority_index
        self._all_devices = all_devices
        self._is_grid = is_grid
        self._attr_native_unit_of_measurement = UnitOfPower.WATT
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_should_poll = False
        self._unsub = []

    async def async_added_to_hass(self):
        async def _update_state(event):
            self.async_write_ha_state()

        for sensor_id in [self._solar_sensor_id, self._device_sensor_id]:
            unsub = async_track_state_change_event(self.hass, [sensor_id], _update_state)
            self._unsub.append(unsub)

    async def async_will_remove_from_hass(self):
        for unsub in self._unsub:
            unsub()
        self._unsub.clear()

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        base_id = self._device_sensor_id.replace(".", "_")
        suffix = "grid" if self._is_grid else "solar"
        return f"solar_split_{base_id}_{suffix}"

    @property
    def state(self):
        solar_state = self.hass.states.get(self._solar_sensor_id)
        device_state = self.hass.states.get(self._device_sensor_id)

        try:
            solar = float(solar_state.state) if solar_state and solar_state.state not in (None, "") else 0
            if solar_state and solar_state.attributes.get("unit_of_measurement") == "kW":
                solar *= 1000
        except (ValueError, TypeError):
            solar = 0

        try:
            device = float(device_state.state) if device_state and device_state.state not in (None, "") else 0
            if device_state and device_state.attributes.get("unit_of_measurement") == "kW":
                device *= 1000
        except (ValueError, TypeError):
            return 0

        prior_usage = 0
        for i, entity in enumerate(self._all_devices):
            if i < self._priority_index and entity and entity.state not in (None, ""):
                try:
                    val = float(entity.state)
                    if entity.attributes.get("unit_of_measurement") == "kW":
                        val *= 1000
                    prior_usage += val
                except (ValueError, TypeError):
                    continue

        remaining_solar = max(solar - prior_usage, 0)
        solar_used = min(remaining_solar, device)
        grid_used = max(device - solar_used, 0)

        return round(grid_used if self._is_grid else solar_used, 2)
