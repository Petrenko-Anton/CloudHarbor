
from django.forms import ModelForm, CharField, TextInput, EmailField, EmailInput, DateField, DateInput, SelectDateWidget
from django import forms
from .models import Contact
from datetime import date

MONTHS = {
    1: "січня",
    2: "лютий",
    3: "березень",
    4: "квітень",
    5: "травень",
    6: "червень",
    7: "липень",
    8: "серпень",
    9: "вересень",
    10: "жовтень",
    11: "листопад",
    12: "грудень",
}


class ContactForm(ModelForm):
    date_range = 70
    this_year = date.today().year

    first_name = CharField(max_length=100, widget=TextInput(
        attrs={'class': "form-control"}))
    last_name = CharField(max_length=100, widget=TextInput(
        attrs={'class': "form-control"}))
    email = EmailField(max_length=100, required=True,
                       widget=EmailInput(attrs={'class': "form-control"}))
    phone = CharField(max_length=100, widget=TextInput(
        attrs={'class': "form-control"}))
    birth_date = DateField(required=True, widget=SelectDateWidget(
        months=MONTHS, years=range(this_year - date_range, this_year+1)))
    description = CharField(max_length=255, widget=forms.Textarea(
        attrs={'class': "form-control"}))

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email',
                  'phone', 'birth_date', 'description')


class SearchContactNameForm(forms.Form):
    search_name = forms.CharField(label="search_name", max_length=100)


class SearchContactEmailForm(forms.Form):
    search_email = forms.EmailField(max_length=100, required=True,
                                    widget=EmailInput(attrs={'class': "form-control"}))
