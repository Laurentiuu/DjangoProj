from django.urls import path
from .views import WeatherListView

urlpatterns = [
    path('', WeatherListView.as_view()),
]