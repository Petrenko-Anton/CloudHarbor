from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

from .forms import ContactForm
from .models import Contact
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# Create your views here.

def index(request):
    return render(request, "contacts/base.html")

def contacts(request):
    return render(request, "contacts/contacts.html")

#add contact_id in params
def addcontact(request):
    form_class = ContactForm
    return render(request, "contacts/addcontact.html", {"form": ContactForm()})

#add contact_id in params
def detailcontact(request):
    return render(request, "contacts/detail.html")

#add contact_id in params
def editcontact(request, contact_id):
    form_class = ContactForm
    return render(request, "contacts/edit.html", {"form": ContactForm()})

#add contact_id in params
def delete_contact(request):
    return render(request, "contacts/delete.html")

