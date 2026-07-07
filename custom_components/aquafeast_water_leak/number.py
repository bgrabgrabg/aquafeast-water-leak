"""Number platform for Aquafeast Water Leak."""

from __future__ import annotations

import asyncio

from homeassistant.components.number import NumberEntity
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
    """Set up Aquafeast numbers."""
    stored = hass.data[DOMAIN][entry.entry_id]
    api = stored["api"]
    coordinator = stored["coordinator"]

    async_add_entities(
        [
            AquafeastWarningMinimumFlowNumber(entry, api, coordinator),
        ]
    )


class AquafeastWarningMinimumFlowNumber(CoordinatorEntity, NumberEntity):
    """Warning minimum flow number entity."""

    _attr_has_entity_name = True
    _attr_name = "warning minimum flow"
    _attr_native_min_value = 1.0
    _attr_native_max_value = 20.0
    _attr_native_step = 0.5
    _attr_native_unit_of_measurement = "L/hr"
    _attr_mode = "slider"

    def __init__(self, entry, api, coordinator) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._api = api
        self._attr_unique_id = f"{entry.entry_id}_warning_minimum_flow"

    @property
    def native_value(self) -> float | None:
        """Return current warning minimum flow."""
        data = self.coordinator.data.get("data", {})
        raw_value = data.get("data22")

        if raw_value in (None, "", "-"):
            return None

        try:
            return float(raw_value) / 10
        except (TypeError, ValueError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        """Set warning minimum flow."""
        await self._api.async_set_warning_minimum_flow(value)
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()
