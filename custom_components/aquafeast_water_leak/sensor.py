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

    async_add_entities(
        [
            AquafeastStatusSensor(coordinator, entry),
            AquafeastProtectionModeSensor(coordinator, entry),
        ]
    )


class AquafeastStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of Aquafeast API status."""

    _attr_has_entity_name = True
    _attr_name = "status"

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_status"

    @property
    def native_value(self):
        """Return the sensor state."""
        return self.coordinator.data.get("resMsg")

    @property
    def extra_state_attributes(self):
        """Return extra state attributes."""
        return self.coordinator.data.get("data", {})


class AquafeastProtectionModeSensor(CoordinatorEntity, SensorEntity):
    """Representation of Aquafeast protection mode."""

    _attr_has_entity_name = True
    _attr_name = "protection mode"
    _attr_icon = "mdi:shield-lock"   # примерно
    
    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_protection_mode"

    @property
    def native_value(self):
        """Return the current protection mode."""
        data = self.coordinator.data.get("data", {})
        raw_mode = data.get("data02")

        if raw_mode is None:
            return None

        try:
            mode = int(raw_mode) - 16
            return f"Mode {mode}"
        except (ValueError, TypeError):
            return raw_mode
