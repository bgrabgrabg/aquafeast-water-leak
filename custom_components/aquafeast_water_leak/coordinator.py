"""Data coordinator for Aquafeast Water Leak."""

from __future__ import annotations

from datetime import timedelta
import logging

import aiohttp

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant

from .const import CONF_DEVICE_MODEL, CONF_MAC, DEFAULT_SCAN_INTERVAL, DOMAIN, GET_STATE_URL

_LOGGER = logging.getLogger(__name__)


class AquafeastDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to manage fetching Aquafeast data."""

    def __init__(self, hass: HomeAssistant, entry_data: dict) -> None:
        """Initialize the coordinator."""
        self.mac_address = entry_data[CONF_MAC]
        self.device_model = entry_data[CONF_DEVICE_MODEL]

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from the BRISK/Aquafeast cloud API."""
        device_id = self.mac_address.replace(":", "").upper()
        url = f"{GET_STATE_URL}?device={device_id}&deviceModel={self.device_model}"

        try:
            session = async_get_clientsession(self.hass)
            async with session.get(url, timeout=15) as response:
                response.raise_for_status()
                data = await response.json()

            if data.get("resCode") != "0":
                raise UpdateFailed(f"API error: {data.get('resMsg')}")

            return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err
