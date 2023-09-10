from django.urls import path
<<<<<<< Updated upstream
from .views import add_contact, index, contacts, editcontact, deletecontact, detailcontact, contact_search_by_name, contact_search_by_email
=======
from .views import add_contact, index, contacts, editcontact, deletecontact, detailcontact, birthlist, contact_search

>>>>>>> Stashed changes
app_name = 'contacts'

urlpatterns = [

    path('', index.as_view(), name='main'),  # contacts:main
    path('contacts', contacts.as_view(), name='contacts'),
<<<<<<< Updated upstream
    path('new-contact', add_contact.as_view(),
         name='addcontact'),
=======
    path('birth-list', birthlist.as_view(), name='birthlist'),
    path('new-contact', add_contact.as_view(), name='addcontact'),
>>>>>>> Stashed changes
    path('detail/<int:contact_id>', detailcontact.as_view(), name="detailcontact"),
    path('edit/<int:contact_id>', editcontact.as_view(), name='editcontact'),
    #     path("contact_list/", contact_list.as_view(),
    #          name="contact_list"),  # for debugging
    path('delete/<int:contact_id>', deletecontact.as_view(), name='deletecontact'),
<<<<<<< Updated upstream
    path('contact_search_by_name', contact_search_by_name.as_view(),
         name="contact_search_by_name"),
    path('contact_search_by_email', contact_search_by_email.as_view(),
         name="contact_search_by_email"),
=======
    path('contact_search', contact_search.as_view(), name="contact_search"),
>>>>>>> Stashed changes
]
