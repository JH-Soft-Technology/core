"""Switch platform for inels."""
import logging

from pyinels.device.pyDoor import pyDoor
from pyinels.device.pySwitch import pySwitch

from homeassistant.components.inels.entity import InelsEntity
from homeassistant.components.switch import SwitchDevice

from .const import (
    DOMAIN,
    DOMAIN_DATA,
    ICON_DOOR,
    ICON_SWITCH,
    PLATFORM_DOOR,
    PLATFORM_SWITCH,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Create new switch device."""
    _LOGGER.info("Setting up switches")

    entities = hass.data[DOMAIN][DOMAIN_DATA]
    coordinator = hass.data[DOMAIN][entry.entry_id]

    devices = [
        dev
        for dev in entities
        if dev.type == PLATFORM_SWITCH or dev.type == PLATFORM_DOOR
    ]

    switches = [
        await hass.async_add_executor_job(pySwitch, dev)
        for dev in devices
        if dev.type == PLATFORM_SWITCH
    ]
    doors = [
        await hass.async_add_executor_job(pyDoor, dev)
        for dev in devices
        if dev.type == PLATFORM_DOOR
    ]

    await coordinator.async_refresh()

    if len(switches) > 0:
        async_add_devices(
            [InelsSwitch(coordinator, switch) for switch in switches], True
        )

    if len(doors) > 0:
        async_add_devices([InelsDoor(coordinator, door) for door in doors], True)


class InelsSwitch(InelsEntity, SwitchDevice):
    """Inels switch class."""

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self.hass.async_add_executor_job(self.device.turn_on)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self.hass.async_add_executor_job(self.device.turn_off)
        await self.coordinator.async_request_refresh()

    @property
    def name(self):
        """Return the name of the switch."""
        return self.device.name

    @property
    def icon(self):
        """Return the icon of this switch."""
        return ICON_SWITCH

    @property
    def is_on(self):
        """Return true if the switch is on."""
        return self.device.state


class InelsDoor(InelsSwitch):
    """Inels door class implements InelsSwitch."""

    @property
    def icon(self):
        """Return the icon of this door."""
        return ICON_DOOR
