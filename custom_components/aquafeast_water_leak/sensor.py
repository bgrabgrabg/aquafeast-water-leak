"""Sensor platform for Aquafeast Water Leak."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Aquafeast sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities([AquafeastRawStatusSensor(coordinator, entry)])


class AquafeastRawStatusSensor(CoordinatorEntity, SensorEntity):
    """Raw status sensor."""

    _attr_has_entity_name = True
    _attr_name = "raw status"

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_raw_status"

    @property
    def native_value(self):
        return self.coordinator.data.get("resMsg", "unknown")

    @property
    def extra_state_attributes(self):
        attrs = {}
        attrs["resCode"] = self.coordinator.data.get("resCode")
        attrs["state"] = self.coordinator.data.get("state")

        data = self.coordinator.data.get("data", {})
        if isinstance(data, dict):
            attrs.update(data)

        return attrs
