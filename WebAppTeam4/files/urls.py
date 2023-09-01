from django.urls import path
from . import views

app_name = 'files'

urlpatterns = [
    path('files/', views.index, name='main'),  # files:main
    ]