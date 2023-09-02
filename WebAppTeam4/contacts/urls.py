from django.urls import path
from . import views
from .views import contact_page_view, add_contact_page_view, contact_list_page_view, contactbook_page_view
app_name = 'contacts'

urlpatterns = [

    path('', views.index, name='main'),  # contacts:main
    path('contacts', views.contacts, name='contacts'),
    path('new-contact', views.addcontact, name='addcontact'),
    #path('detail/<int:contact_id>', views.detailcontact, name="detailcontact"),
    path('edit/<int:contact_id>', views.editcontact, name='editcontact'),
    #path('delete/<int:contact_id>', views.deletecontact, name='deletecontact'),
    ]

