from homeassistant import config_entries
import homeassistant.helpers.config_validation as cv
import logging
import voluptuous as vol
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class PresenceSimulationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2
    data = None
    async def async_create_flow(handler, context, data):
            """Create flow."""
    async def async_finish_flow(flow, result):
            """Finish flow."""
    async def async_step_user(self, info=None):
        data_schema = {
            vol.Required("switch", description={"suggested_value": "Choose a unique name"}): str,
            vol.Required("entities"): str, #cv.entity_ids,
            vol.Required("delta", default=7): int,
            vol.Required("interval", default=30): int,
            vol.Required("restore", default=False): bool,
            vol.Required("random", default=0): int,
        }
        if not info:
            return self.async_show_form(
                step_id="user", data_schema=vol.Schema(data_schema)
            )
        self.data = info
        try:
            _LOGGER.debug("info.entities %s",info['entities'])
            #check if entity exist
            #hass.states.get(info['entities'])
        except Exception as e:
            _LOGGER.debug("Exception %s", e)
            return self.async_show_form(
                step_id="user", data_schema=vol.Schema(data_schema)
            )
        else:
            return self.async_create_entry(title="Simulation Presence", data=self.data)

    #@callback
    @staticmethod
    def async_get_options_flow(entry):
        _LOGGER.debug("entry %s", entry)
        return OptionsFlowHandler(entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, info=None):
        errors: Dict[str, str] = {}
        _LOGGER.debug("config flow init %s", info)

        if "interval" in self.config_entry.data:
            interval = self.config_entry.data["interval"]
        else:
            interval = 30
        if "restore" in self.config_entry.data:
            restore = self.config_entry.data["restore"]
        else:
            restore = 0
        if "random" in self.config_entry.data:
            random = self.config_entry.data["random"]
        else:
            random = 0

        data_schema = {
            vol.Required("switch", default=self.config_entry.data["switch"]): str,
            vol.Required("entities", default=self.config_entry.data["entities"]): str,
            vol.Required("delta", default=self.config_entry.data["delta"]): int,
            vol.Required("interval", default=interval): int,
            vol.Required("restore", default=restore): bool,
            vol.Required("random", default=random): int,
        }
        _LOGGER.debug("switch %s", self.config_entry.data["switch"])
        _LOGGER.debug("config_entry data %s", self.config_entry.data)
        _LOGGER.debug("will async_show_form")

        if not info:
            return self.async_show_form(
                step_id="init", data_schema=vol.Schema(data_schema)
            )

        #if pop-up is saved but the name has changed, log an error and ask again
        if info["switch"] != self.config_entry.data["switch"]:
            _LOGGER.error("Presence Simulation Switch name can't be changed")
            errors["base"] = "cannot_change_name"
            return self.async_show_form(
                step_id="init", data_schema=vol.Schema(data_schema), errors=errors
            )

        return self.async_create_entry(title="Simulation Presence", data=info)
        #return self.async_create_entry(title=self.config_entry.data["switch"], data=info)
