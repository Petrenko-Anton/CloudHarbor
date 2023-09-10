from django.urls import path
from .views import add_contact, index, contacts, editcontact, deletecontact, detailcontact, birthlist, contact_search

app_name = 'contacts'

urlpatterns = [

    path('', index.as_view(), name='main'),  # contacts:main
    path('contacts', contacts.as_view(), name='contacts'),
    path('birth-list', birthlist.as_view(), name='birthlist'),
    path('new-contact', add_contact.as_view(), name='addcontact'),
    path('detail/<int:contact_id>', detailcontact.as_view(), name="detailcontact"),
    path('edit/<int:contact_id>', editcontact.as_view(), name='editcontact'),
    #     path("contact_list/", contact_list.as_view(),
    #          name="contact_list"),  # for debugging
    path('delete/<int:contact_id>', deletecontact.as_view(), name='deletecontact'),
    path('contact_search', contact_search.as_view(), name="contact_search"),
]
