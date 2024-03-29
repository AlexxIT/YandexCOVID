import json
import logging
import re
from datetime import datetime

from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.typing import HomeAssistantType

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'yandex_covid'

RE_HTML = re.compile(r'class="state-view">(.+?)<')
RE_TIME = re.compile(r', (.+?) \(')


async def async_setup_platform(hass: HomeAssistantType, config, add_entities,
                               discovery_info=None):
    include = config.get('include')
    add_entities([YandexCovid(include)])

    return True


class YandexCovid(Entity):
    def __init__(self, include: list):
        self._attrs = None
        self._state = None
        self.include = include
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
        data = token = None

        try:
            r = await self.session.get('https://yandex.ru/web-maps/covid19')
            text = await r.text()

            m = RE_HTML.search(text)
            data = json.loads(m[1])
            # token = data['csrfToken']
            data = data['config']['covidData']

        except Exception as e:
            _LOGGER.error(f"Load Data error: {e}")

        try:
            items = [p for p in data['items'] if p['name'] in self.include] \
                    if self.include else data['items']

            self._attrs = {
                p['name']: {
                    'cases': p['cases'],
                    'cured': p['cured'],
                    'deaths': p['deaths'],
                    'new_cases': (p['histogram'][-1]['value'] -
                                  p['histogram'][-2]['value'])
                    if 'histogram' in p and len(p['histogram']) >= 2 else 0
                }
                for p in items
            }

        except Exception as e:
            _LOGGER.error(f"Update Places error: {e}")

        if not self.include or 'Россия' in self.include:
            try:
                self._attrs['Россия'] = ru = {
                    'cases': 0,
                    'cured': 0,
                    'deaths': 0,
                    'new_cases': (data['histogram'][-1]['value'] -
                                  data['histogram'][-2]['value']),
                    # 'tests': int(data['tests'].replace(' ', ''))
                }
                for p in data['items']:
                    if p.get('ru'):
                        ru['cases'] += p['cases']
                        ru['cured'] += p['cured']
                        ru['deaths'] += p['deaths']

            except Exception as e:
                _LOGGER.error(f"Update Russia error: {e}")

        if not self.include or 'Мир' in self.include:
            try:
                self._attrs['Мир'] = world = {
                    'cases': 0,
                    'cured': 0,
                    'deaths': 0
                }
                for p in data['items']:
                    if 'ru' not in p:
                        world['cases'] += p['cases'] or 0
                        world['cured'] += p['cured'] or 0
                        world['deaths'] += p['deaths'] or 0

            except Exception as e:
                _LOGGER.error(f"Update World error: {e}")

        try:
            ts = datetime.fromtimestamp(data['ts'])
            self._state = ts.strftime("%H:%M")

        except Exception as e:
            _LOGGER.error(f"Update Sensor error: {e}")

        # try:
        #     r = await self.session.get(
        #         'https://yandex.ru/maps/api/covid',
        #         params={'csrfToken': token, 'isolation': 'true'})
        #     a = await r.read()
        #     data = await r.json()
        #
        #     if self.include:
        #         data['data']['cities'] = [p for p in data['data']['cities']
        #                                   if p['name'] in self.include]
        #
        #     for city in data['data']['cities']:
        #         name = city['name']
        #         if name in self._attrs:
        #             self._attrs[name]['isolation'] = city['level']
        #         else:
        #             self._attrs[name] = {'isolation': city['level']}
        #
        # except Exception as e:
        #     _LOGGER.error(f"Update Isolation error: {e}")

        self.async_schedule_update_ha_state()

        async_call_later(self.hass, 60 * 60, self.update)
