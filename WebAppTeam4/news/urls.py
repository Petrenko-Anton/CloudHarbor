from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='main'),
    path('get_weather/', views.get_weather, name='get_weather'),
]