from rest_framework import serializers
from .models import Weather


class WheatherSerializers(serializers.ModelSerializer):
    class MetaData:
        model = Weather
        fields = (
            'airTemperature', 'pressure', 'humidity',
            'precipitation', 'visibility', 'weatherTemperature',
            'windDirection', 'windSpeed', 'waveHeight')
