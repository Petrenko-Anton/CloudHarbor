from django.forms import ModelForm, CharField, TextInput, DateField, EmailField
from .models import Contact

    # name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # birth_date = models.DateField()
    # phone = models.CharField(max_length=16)
    # email = models.EmailField()
    # is_favorite = models.BooleanField(default=False)
    # description = models.TextField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)


class ContactForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    last_name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    birth_date = DateField();
    phone = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    email = EmailField()
    description = CharField(widget=TextArea())

    class Meta:
        model = Contact
        fields = ["name", "last_name","birth_date","phone","email","description"]