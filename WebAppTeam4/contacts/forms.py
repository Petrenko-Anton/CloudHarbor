from django.forms import ModelForm, CharField, TextInput, EmailField, EmailInput, DateField, SelectDateWidget
from django import forms

from .models import Contact
from datetime import date

MONTHS = {
    1: "Січень",
    2: "Лютий",
    3: "Березень",
    4: "Квітень",
    5: "Травень",
    6: "Червень",
    7: "Липень",
    8: "Серпень",
    9: "Вересень",
    10: "Жовтень",
    11: "Листопад",
    12: "Грудень",
}

class ContactForm(ModelForm):
    first_name = CharField(max_length=100, widget=TextInput(
        attrs={'class': "form-control"}))
    last_name = CharField(max_length=100, widget=TextInput(
        attrs={'class': "form-control"}))
    email = EmailField(max_length=100, required=True,
                       widget=EmailInput(attrs={'class': "form-control"}))
    phone = CharField(max_length=100, widget=TextInput(
        attrs={'class': "form-control"}))
    birth_date = DateField(
        required=True, widget=SelectDateWidget(months=MONTHS, 
                                               years=[x for x in range(date.today().year - 100, date.today().year + 1)]))
    description = CharField(required = False, max_length=255, widget=forms.Textarea(
        attrs={'class': "form-control"}))

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'description')

class SearchContactNameForm(forms.Form):
    search_name = forms.CharField(label="search_name", max_length=100, required=True,
                                    widget=TextInput(attrs={'class': "form-control"}))

class SearchContactEmailForm(forms.Form):
    search_email = forms.EmailField(max_length=100, required=True,
                                    widget=EmailInput(attrs={'class': "form-control"}))
