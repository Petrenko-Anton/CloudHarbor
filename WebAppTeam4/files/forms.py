from django.forms import ModelForm, CharField, FileInput, TextInput, FileField

from .models import File


class FileForm(ModelForm):
    description = CharField(max_length=255, widget=TextInput(attrs={"class": "form-control"}))
    path = FileField(widget=FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = File
        fields = ['description', 'path']