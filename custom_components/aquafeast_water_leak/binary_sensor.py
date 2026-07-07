"""Binary sensor platform for Aquafeast Water Leak."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
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
    """Set up Aquafeast binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities(
        [
            AquafeastValveBinarySensor(coordinator, entry),
        ]
    )


class AquafeastValveBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of Aquafeast valve state."""

    _attr_has_entity_name = True
    _attr_name = "valve"
    _attr_device_class = "opening"

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_valve"

    @property
    def is_on(self):
        """Return true if valve is open."""
        data = self.coordinator.data.get("data", {})
        return data.get("data01") == "1"
