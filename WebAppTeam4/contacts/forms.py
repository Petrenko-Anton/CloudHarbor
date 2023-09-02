
from django.forms import ModelForm, CharField, TextInput, EmailField, EmailInput, DateField, DateInput

from .models import Contact


class ContactForm(ModelForm):

    first_name = CharField(max_length=100, widget=TextInput(attrs={'class': "form-control"}))
    last_name = CharField(max_length=100, widget=TextInput(attrs={'class': "form-control"}))
    email = EmailField(max_length=100, required=True, widget=EmailInput(attrs={'class': "form-control"}))
    phone = CharField(max_length=100, widget=TextInput(attrs={'class': "form-control"}))
    birth_date = DateField(required=True, widget=DateInput(attrs={'class': "form-control"}))
    comment = CharField(max_length=100, widget=TextInput(attrs={'class': "form-control"})) 

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date')

