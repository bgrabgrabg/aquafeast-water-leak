"""Button platform for Aquafeast Water Leak."""

from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Aquafeast buttons."""
    stored = hass.data[DOMAIN][entry.entry_id]
    api = stored["api"]
    coordinator = stored["coordinator"]

    async_add_entities(
        [
            AquafeastCommandButton(
                entry,
                api,
                coordinator,
                "01",
                "1",
                "valve key01 value1",
            ),
            AquafeastCommandButton(
                entry,
                api,
                coordinator,
                "01",
                "0",
                "valve key01 value0",
            ),
        ]
    )


class AquafeastCommandButton(ButtonEntity):
    """Generic command button."""

    _attr_has_entity_name = True

    def __init__(self, entry, api, coordinator, key: str, value: str, name: str) -> None:
        self._entry = entry
        self._api = api
        self._coordinator = coordinator
        self._key = key
        self._value = value
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}_{value}"

    async def async_press(self) -> None:
        await self._api.async_send_command(self._key, self._value)
        await self._coordinator.async_request_refresh()
