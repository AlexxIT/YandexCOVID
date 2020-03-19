import json
import logging
import re

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.typing import HomeAssistantType

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'yandex_covid'

RE_HTML = re.compile(r'class="config-view">(.+?)<')
RE_TIME = re.compile(r', (.+?) \(')


async def async_setup_platform(hass: HomeAssistantType, config, add_entities,
                               discovery_info=None):
    add_entities([YandexCovid()])

    return True


class YandexCovid(Entity):
    def __init__(self):
        self._attrs = None
        self._state = None
        self.session = None

    async def async_added_to_hass(self) -> None:
        self.session = async_get_clientsession(self.hass)
        self.hass.async_create_task(self.update())

    @property
    def should_poll(self) -> bool:
        return False

    @property
    def unique_id(self):
        return DOMAIN

    @property
    def name(self):
        return "Yandex COVID"

    @property
    def state(self):
        return self._state

    @property
    def state_attributes(self):
        return self._attrs

    async def update(self, *args):
        try:
            r = await self.session.get('https://yandex.ru/web-maps/covid19')
            text = await r.text()

            m = RE_HTML.search(text)
            data = json.loads(m[1])

            self._attrs = {
                p['name']: {
                    'cases': p['cases'],
                    'cured': p['cured'],
                    'deaths': p['deaths']
                }
                for p in data['covidData']['items']
            }

            items = data['covidData']['stat']['items']
            self._attrs['Россия'] = {
                'cases': int(items[0]['value']),
                'new_cases': int(items[1]['value']),
                'cured': int(items[2]['value']),
                'deaths': int(items[3]['value'])
            }

            m = re.search(r', (.+?) \(', data['covidData']['subtitle'])
            self._state = m[1]

        except Exception as e:
            _LOGGER.error(f"Update error: {e}")

        self.async_schedule_update_ha_state()

        async_call_later(self.hass, 60 * 60, self.update)
