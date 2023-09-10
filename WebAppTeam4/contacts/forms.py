from django.forms import ModelForm, CharField, TextInput, EmailField, EmailInput, DateField, SelectDateWidget
from datetime import date
from django import forms

from .models import Contact

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
    date_range = 70    
    this_year = date.today().year
    
    first_name = CharField(max_length=100, widget=TextInput(attrs={'class': "form-control"}))
    last_name = CharField(max_length=100, widget=TextInput(attrs={'class': "form-control"}))
    email = EmailField(max_length=100, required=True, widget=EmailInput(attrs={'class': "form-control"}))
    phone = CharField(max_length=100, widget=TextInput(attrs={'class': "form-control"}))
    birth_date = DateField(required=True, widget=SelectDateWidget(months=MONTHS, years=range(this_year - date_range, this_year+1)))
    description = CharField(max_length=255, widget=TextInput(attrs={'class': "form-control"}))


    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'description')


class SearchContactNameForm(forms.Form):
    search_name = forms.CharField(label="search_name", max_length=100)
