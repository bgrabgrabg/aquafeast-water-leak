"""Number platform for Aquafeast Water Leak."""

from __future__ import annotations

import asyncio

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONF_MAC, DOMAIN, MANUFACTURER, MODEL


def _is_imperial(data: dict) -> bool:
    return str(data.get("data09")) == "1"


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
    _attr_mode = "slider"

    def __init__(self, entry, api, coordinator) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._api = api
        self._attr_unique_id = f"{entry.entry_id}_warning_minimum_flow"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer=MANUFACTURER,
            model=MODEL,
            name=entry.title,
            serial_number=entry.data.get(CONF_MAC),
        )

    @property
    def _data(self) -> dict:
        return self.coordinator.data.get("data", {})

    @property
    def native_unit_of_measurement(self):
        return "GPM" if _is_imperial(self._data) else "L/hr"

    @property
    def native_min_value(self) -> float:
        return 0.01 if _is_imperial(self._data) else 1.0

    @property
    def native_max_value(self) -> float:
        return 0.20 if _is_imperial(self._data) else 20.0

    @property
    def native_step(self) -> float:
        return 0.01 if _is_imperial(self._data) else 0.5

    @property
    def native_value(self) -> float | None:
        """Return current warning minimum flow."""
        raw_value = self._data.get("data22")

        if raw_value in (None, "", "-"):
            return None

        try:
            raw = float(raw_value)
        except (TypeError, ValueError):
            return None

        if _is_imperial(self._data):
            return round(raw / 1000, 2)

        return round(raw / 10, 1)

    async def async_set_native_value(self, value: float) -> None:
        """Set warning minimum flow."""
        await self._api.async_set_warning_minimum_flow(value)
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()
