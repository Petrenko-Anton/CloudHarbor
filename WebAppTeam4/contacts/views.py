from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

from .forms import ContactForm
from .models import Contact
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class index(View):
    template_name = "contacts/base.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class contacts(View):
    template_name = "contacts/contacts.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# add contact_id in params
@method_decorator(login_required, name="dispatch")
class add_contact(View):
    form_class = ContactForm
    initial = {"key": "value"}
    template_name = "contacts/addcontact.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_contact = form.save(commit=False)
            new_contact.user = request.user
            new_contact.save()
            return redirect(to="contacts:main")
        else:
            # messages.error(request, 'Input error')
            return render(request, self.template_name, {"form": form})


# def addcontact(request):
#     form_class = ContactForm
#     return render(request, "contacts/addcontact.html", {"form": ContactForm()})

# add contact_id in params


def detailcontact(request):
    return render(request, "contacts/detail.html")

# add contact_id in params


@method_decorator(login_required, name="dispatch")
class editcontact(View):
    template_name = "contacts/edit.html"
    form_class = ContactForm
    initial = {"key": "value"}

    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, contact_id):
        form = self.form_class(initial=self.initial)
        contact = Contact.objects.get(pk=contact_id)
        return render(request, self.template_name, {"form": form, "contact": contact})

    def post(self, request, contact_id):
        form = self.form_class(request.POST)
        contact = Contact.objects.get(pk=contact_id)

        if form.is_valid():
            updated_contact = form.save(commit=False)
            updated_contact.user = request.user
            Contact.objects.filter(pk=contact_id).update(
                email=updated_contact.email,
                phone=updated_contact.phone,
                first_name=updated_contact.first_name,
                last_name=updated_contact.last_name,
                birth_date=updated_contact.birth_date)

            return redirect(to="contacts:contacts")
        else:
            # messages.error(request, 'Input error')
            return render(request, self.template_name, {"form": form, "contact": contact})


# def editcontact(request, contact_id):
#     form_class = ContactForm
#     contact = Contact.objects.get(pk=contact_id)
#     return render(request, "contacts/edit.html", {"form": ContactForm(), "contact": contact})

# add contact_id in params
@method_decorator(login_required, name="dispatch")
class deletecontact(View):
    template_name = "contacts/contact_list.html"

    def get(self, request, contact_id):
        Contact.objects.get(pk=contact_id).delete()
        contacts = (
            Contact.objects.filter(user=request.user).all()
            if request.user.is_authenticated
            else []
        )
        return render(request, self.template_name, {"contacts": contacts})


# from Django documentation
# b = Blog.objects.get(pk=1)
# # This will delete the Blog and all of its Entry objects.
# b.delete()


@method_decorator(login_required, name="dispatch")
class contact_list(View):
    template_name = "contacts/contact_list.html"

    def get(self, request, *args, **kwargs):
        contacts = (
            Contact.objects.filter(user=request.user).all()
            if request.user.is_authenticated
            else []
        )
        return render(request, self.template_name, {"contacts": contacts})
