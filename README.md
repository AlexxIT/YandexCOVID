# Yandex COVID-19

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Сенсор по данным Яндекса: https://yandex.ru/web-maps/covid19

Основные моменты:
- есть **региональная статистика**, есть ли ваш регион - смотрите на карте Яндекса
- статистика не по городам, а по регионам! Москва и Санкт-Петербург исключения
- есть количество **проведённых тестов** по стране
- есть **индекс самоизоляции** и он **по городам**, есть ли ваш город - смотрите на карте Яндекса

## Установка и настройка

Устанавливается через HACS.

Настраивается в `configuration.yaml`:

`include` - опциональный параметр, без него сенсор будет хранить данные по всему миру, что приводит к ошибкам переполнения БД у некоторых пользователей

```yaml
sensor:
- platform: yandex_covid
  include:
    - Россия
    - Москва
    - Самарская область
    - Самара
    - Тольятти

- platform: template
  sensors:
    covid_russia_cases:
      friendly_name: Заражений в России
      icon_template: mdi:emoticon-neutral-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Россия')['cases'] }}"
    covid_russia_cured:
      friendly_name: Выздоровлений в России
      icon_template: mdi:emoticon-happy-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Россия')['cured'] }}"
    covid_russia_deaths:
      friendly_name: Смертей в России
      icon_template: mdi:emoticon-dead-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Россия')['deaths'] }}"
    covid_russia_new_cases:
      friendly_name: Новых случаев в России
      icon_template: mdi:emoticon-cry-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Россия')['new_cases'] }}"
    covid_russia_tests:
      friendly_name: Проведено тестов в России
      icon_template: mdi:test-tube
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Россия')['tests'] }}"

    covid_moscow_cases:
      friendly_name: Заражений в Москве
      icon_template: mdi:emoticon-neutral-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Москва')['cases'] }}"
    covid_moscow_cured:
      friendly_name: Выздоровлений в Москве
      icon_template: mdi:emoticon-happy-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Москва')['cured'] }}"
    covid_moscow_deaths:
      friendly_name: Смертей в Москве
      icon_template: mdi:emoticon-dead-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Москва')['deaths'] }}"
    covid_moscow_isolation:
      friendly_name: Индекс самоизоляции Москвы
      icon_template: mdi:home-lock
      unit_of_measurement: " "
      value_template: "{{ state_attr('sensor.yandex_covid', 'Москва')['isolation'] }}"

    covid_samara_cases:
      friendly_name: Заражений в Самарской области
      icon_template: mdi:emoticon-neutral-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Самарская область')['cases'] }}"
    covid_samara_cured:
      friendly_name: Выздоровлений в Самарской области
      icon_template: mdi:emoticon-happy-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Самарская область')['cured'] }}"
    covid_samara_deaths:
      friendly_name: Смертей в Самарской области
      icon_template: mdi:emoticon-dead-outline
      unit_of_measurement: people
      value_template: "{{ state_attr('sensor.yandex_covid', 'Самарская область')['deaths'] }}"

    covid_samara_isolation:
      friendly_name: Индекс самоизоляции Самары
      icon_template: mdi:home-lock
      unit_of_measurement: " "
      value_template: "{{ state_attr('sensor.yandex_covid', 'Самара')['isolation'] }}"
    covid_tolyatti_isolation:
      friendly_name: Индекс самоизоляции Тольятти
      icon_template: mdi:home-lock
      unit_of_measurement: " "
      value_template: "{{ state_attr('sensor.yandex_covid', 'Тольятти')['isolation'] }}"
```