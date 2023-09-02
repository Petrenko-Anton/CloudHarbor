from django.urls import path
from . import views
from .views import contact_page_view, add_contact_page_view, contact_list_page_view, contactbook_page_view
app_name = 'contacts'

urlpatterns = [
    # path('', views.index, name='main'),  # contacts:main
    path('', contact_page_view.as_view(), name='main'),  # contacts:main
    path('add_contact/', add_contact_page_view.as_view(), name='add_contact'),
    path('contact_list/', contact_list_page_view.as_view(), name='contact_list'),
    path('contactbook/', contactbook_page_view.as_view(), name='contactbook')
]
