from django.urls import path
from . import views
from .views import contact_page_view
app_name = 'contacts'

urlpatterns = [
    # path('', views.index, name='main'),  # contacts:main
    path('', contact_page_view.as_view(), name='main'),  # contacts:main
    ]