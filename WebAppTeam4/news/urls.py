from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='main'),
    # path('<str:category>', views.index, name='main'),
    # path('<str:city>', views.index, name='weather'),
    ]