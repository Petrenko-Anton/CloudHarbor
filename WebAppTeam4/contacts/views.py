from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Contact
from django.views.generic.base import TemplateView

# Create your views here.
class contact_page_view(TemplateView):
    template_name = "contacts/index.html"

# def index(request):
#      return render(request, 'contacts/index.html')
