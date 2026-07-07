"""Switch platform for Aquafeast Water Leak."""

from __future__ import annotations

import asyncio

from homeassistant.components.switch import SwitchEntity
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
    """Set up Aquafeast switches."""
    stored = hass.data[DOMAIN][entry.entry_id]
    api = stored["api"]
    coordinator = stored["coordinator"]

    async_add_entities(
        [
            AquafeastValveSwitch(entry, api, coordinator),
        ]
    )


class AquafeastValveSwitch(CoordinatorEntity, SwitchEntity):
    """Valve switch with real state feedback."""

    _attr_has_entity_name = True
    _attr_name = "water valve"

    def __init__(self, entry, api, coordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._entry = entry
        self._api = api
        self._attr_unique_id = f"{entry.entry_id}_water_valve"

    @property
    def is_on(self) -> bool | None:
        """Return valve state."""
        data = self.coordinator.data.get("data", {})
        value = data.get("data01")

        if value is None:
            return None

        return str(value) == "1"

    async def async_turn_on(self, **kwargs) -> None:
        """Open valve."""
        await self._api.async_send_command("01", "1")
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        """Close valve."""
        await self._api.async_send_command("01", "0")
        await asyncio.sleep(2)
        await self.coordinator.async_request_refresh()
