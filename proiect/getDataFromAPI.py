import json
from datetime import datetime, timezone
from pprint import pprint
from .models import Weather

import requests


def getData(days):
    # iau date din 2018
    past = datetime.fromtimestamp(days, tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)
    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={'lat': 38.7984,
                'lng': 17.8081,
                # daca pun alta ordine nu imi afiseaza cum trebuie. am luat inordinea din documentatie
                'params': ','.join(['airTemperature', 'pressure', 'cloudCover', 'currentDirection',
                                    'currentSpeed', 'gust', 'humidity', 'precipitation',
                                    'snowDepth', 'swellDirection', 'swellHeight',
                                    'swellHeight', 'swellPeriod', 'visibility', 'waterTemperature',
                                    'waveDirection', 'waveHeight', 'wavePeriod', 'windWaveDirection',
                                    'windWaveHeight', 'windWavePeriod', 'windDirection', 'windSpeed']),
                'start': past,
                'end': now,
                # iau doar sg
                'source': 'sg'
                },
        headers={'Authorization': 'a6237776-c6f8-11eb-80ed-0242ac130002-a6237802-c6f8-11eb-80ed-0242ac130002'}
    )

    jsonData = response.json()
    # pprint(jsonData)
    with open('date.json', 'a') as jsonFile:
        json.dump(jsonData, jsonFile)

    key = jsonData['hours']
    for data in key:
        airTemperature = data['airTemperature']['sg']
        pressure = data['pressure']['sg']
        humidity = data['humidity']['sg']
        precipitation = data['precipitation']['sg']
        visibility = data['visibility']['sg']
        waterTemperature = data['waterTemperature']['sg']
        windDirection = data['windDirection']['sg']
        windSpeed = data['windSpeed']['sg']
        weather = Weather(airTemperature=airTemperature, pressure=pressure,
                          humidity=humidity, precipitation=precipitation,
                          visibility=visibility, waterTemperature=waterTemperature,
                          windDirection=windDirection, windSpeed=windSpeed)

        weather.save()
        return weather
