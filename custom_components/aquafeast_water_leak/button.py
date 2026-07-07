"""Button platform for Aquafeast Water Leak."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    stored = hass.data[DOMAIN][entry.entry_id]
    api = stored["api"]
    coordinator = stored["coordinator"]

    async_add_entities(
        [
            AquafeastSyncClockButton(entry, api, coordinator),
        ]
    )


class AquafeastSyncClockButton(ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = "sync clock"

    def __init__(self, entry, api, coordinator) -> None:
        self._entry = entry
        self._api = api
        self._coordinator = coordinator
        self._attr_unique_id = f"{entry.entry_id}_sync_clock"

    async def async_press(self) -> None:
        now = dt_util.now()
        await self._api.async_set_clock(now.hour, now.minute, now.second)
        await self._coordinator.async_request_refresh()
