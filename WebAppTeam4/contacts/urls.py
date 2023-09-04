from django.urls import path
from .views import add_contact, index, contacts, editcontact, contact_list
app_name = 'contacts'

urlpatterns = [

    path('', index.as_view(), name='main'),  # contacts:main
    path('contacts', contacts.as_view(), name='contacts'),
    path('new-contact', add_contact.as_view(),
         name='addcontact'),
    #path('detail/<int:contact_id>', views.detailcontact, name='detailcontact'),
    #path('edit/<int:contact_id>', editcontact.as_view(), name='editcontact'),
    path('contacts/', contact_list.as_view(), name='contacts'),  # for debugging
    #path('delete/<int:contact_id>', views.deletecontact, name='deletecontact'),
]
