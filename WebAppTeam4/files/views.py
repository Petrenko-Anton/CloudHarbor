from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    return render(request, 'files/files.html')
