from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Contact
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.

# def index(request):
#      return render(request, 'contacts/index.html')


class contact_page_view(TemplateView):
    template_name = "contacts/index.html"


class add_contact_page_view(CreateView):
    template_name = "contacts/add_contact.html"
    model = Contact
    fields = ["name", "last_name", "birth_date",
              "phone", "email", "description"]


class contact_list_page_view(TemplateView):
    template_name = "contacts/contact_list.html"


class contactbook_page_view(TemplateView):
    template_name = "contacts/contactbook.html"
