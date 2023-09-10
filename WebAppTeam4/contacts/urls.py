from django.urls import path

from .views import add_contact, index, contacts, edit_contact, delete_contact, detailcontact, contact_search_by_name, \
    contact_search_by_email, birthlist, contact_search

app_name = 'contacts'

urlpatterns = [

    path('', index.as_view(), name='main'),  # contacts:main
    path('contacts', contacts.as_view(), name='contacts'),
    path('birth-list', birthlist.as_view(), name='birthlist'),
    path('new-contact', add_contact.as_view(),name='addcontact'),
    path('detail/<int:contact_id>', detailcontact.as_view(), name="detailcontact"),
    path('edit/<int:contact_id>', edit_contact.as_view(), name='editcontact'),
    path('delete/<int:contact_id>', delete_contact.as_view(), name='deletecontact'),

    path('contact_search_by_name', contact_search_by_name.as_view(),
         name="contact_search_by_name"),
    path('contact_search_by_email', contact_search_by_email.as_view(),
         name="contact_search_by_email"),

    path('contact_search', contact_search.as_view(), name="contact_search"),
]
