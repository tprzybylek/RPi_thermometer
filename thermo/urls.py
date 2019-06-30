from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='thermo_dashboard'),
    # path('outdoor_aqi/', views.get_outdoor_air_quality, name='outdoor_aqi'),
    # path('outdoor_meteo/', views.get_weather, name='outdoor_meteo'),
]