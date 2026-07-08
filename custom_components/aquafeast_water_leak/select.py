"""Select platform for Aquafeast Water Leak."""

from __future__ import annotations

import asyncio

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

MODE_MAP = {
    "UnProtect": 1,
    "Mode 1": 17,
    "Mode 2": 18,
    "Mode 3": 19,
}

MODE_REVERSE = {v: k for k, v in MODE_MAP.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Aquafeast selects."""
    stored = hass.data[DOMAIN][entry.entry_id]
    api = stored["api"]
    coordinator = stored["coordinator"]

    async_add_entities(
        [
            AquafeastOperationModeSelect(entry, api, coordinator),
        ]
    )


class AquafeastOperationModeSelect(CoordinatorEntity, SelectEntity):
    """Operation mode select entity."""

    _attr_has_entity_name = True
    _attr_name = "operation mode"
    _attr_options = list(MODE_MAP.keys())

    def __init__(self, entry, api, coordinator) -> None:
        """Initialize the select entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._api = api
        self._attr_unique_id = f"{entry.entry_id}_operation_mode"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            manufacturer="Aquafeast",
            name=f"Aquafeast {self._entry.title}",
            model="Water Leak Controller",
            serial_number=self._entry.data.get("mac"),
        )

    @property
    def current_option(self) -> str | None:
        """Return current operation mode."""
        data = self.coordinator.data.get("data", {})
        raw_value = data.get("data02")

        if raw_value is None:
            return None

        try:
            code = int(raw_value)
        except (TypeError, ValueError):
            return None

        if code == 1:
            return "UnProtect"

        return MODE_REVERSE.get(code)

    async def async_select_option(self, option: str) -> None:
        """Set operation mode."""
        mode_code = MODE_MAP.get(option)
        if mode_code is None:
            return

        await self._api.async_set_mode(mode_code, flow_set=0)
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()
