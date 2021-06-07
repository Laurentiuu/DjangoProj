from datetime import timezone, datetime

from django.db import models

##declar datele primite de la API

class Weather(models.Model):
    airTemperature = models.FloatField(default=0)
    pressure = models.FloatField(default=0)
    humidity = models.FloatField(default=0)
    precipitation = models.FloatField(default=0)
    visibility = models.FloatField(default=0)
    waterTemperature = models.FloatField(default=0)
    windDirection = models.FloatField(default=0)
    windSpeed = models.FloatField(default=0)

    def createDict(self):
        return {
            'airTemperature': self.airTemperature,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'precipitation': self.precipitation,
            'visibility': self.visibility,
            'waterTemperature': self.waterTemperature,
            'windDirection': self.windDirection,
            'windSpeed': self.windSpeed,
        }

    def __str__(self, data=None):
        return 'data'
