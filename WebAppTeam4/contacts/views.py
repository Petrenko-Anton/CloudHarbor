from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

from .forms import ContactForm, SearchContactNameForm, SearchContactEmailForm
from .models import Contact
from django.views import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
# Create your views here.


class index(View):
    template_name = "contacts/base.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required, name="dispatch")
class contacts(View):
    template_name = "contacts/contacts.html"

    def get(self, request, *args, **kwargs):
        search_form = SearchContactNameForm()
        contacts = (
            Contact.objects.filter(user=request.user).all()
            if request.user.is_authenticated
            else []
        )
        return render(request, self.template_name, {"contacts": contacts, "form": search_form})


@method_decorator(login_required, name="dispatch")
class birthlist(View):
    template_name = "contacts/contacts.html"

    def get(self, request, *args, **kwargs):
        search_form = SearchContactNameForm()
        contacts = (
            Contact.objects.filter(user=request.user).all()
            if request.user.is_authenticated
            else []
        )
        return render(request, self.template_name, {"contacts": contacts, "form": search_form})


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
            return redirect(to="contacts:contacts")
        else:
            # messages.error(request, 'Input error')
            return render(request, self.template_name, {"form": form})


@method_decorator(login_required, name="dispatch")
class detailcontact(View):
    template_name = "contacts/detail.html"

    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)
    def get(self, request, contact_id):
        contact = Contact.objects.get(pk=contact_id)
        return render(request, self.template_name, {"contact": contact})
# add contact_id in params


@method_decorator(login_required, name="dispatch")
class editcontact(View):
    template_name = "contacts/edit.html"
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, contact_id):
        contact = Contact.objects.get(pk=contact_id)
        default_settings = {"first_name": contact.first_name,
                            "last_name": contact.last_name,
                            "email": contact.email,
                            "birth_date": contact.birth_date,
                            "phone": contact.phone,
                            "description": contact.description,
                            }

        form = ContactForm(initial=default_settings)

        return render(request, self.template_name, {"form": form, "contact": contact})

    def post(self, request, contact_id):
        form = ContactForm(request.POST)
        contact = Contact.objects.get(pk=contact_id)

        if form.is_valid():
            updated_contact = form.save(commit=False)
            updated_contact.user = request.user
            Contact.objects.filter(pk=contact_id).update(
                email=updated_contact.email,
                phone=updated_contact.phone,
                first_name=updated_contact.first_name,
                last_name=updated_contact.last_name,
                birth_date=updated_contact.birth_date,
                description=updated_contact.description)

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
    template_name = "contacts/delete.html"

    def get(self, request, contact_id):
        Contact.objects.get(pk=contact_id).delete()
        contacts = (
            Contact.objects.filter(user=request.user).all()
            if request.user.is_authenticated
            else []
        )
        return render(request, self.template_name, {"contacts": contacts})


@method_decorator(login_required, name="dispatch")
class contact_search(View):
    template_name = "contacts/contacts.html"

    def get(self, request, *args, **kwargs):
        form = SearchContactNameForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data["search_name"]
            contacts = (Contact.objects.filter(Q(user=request.user), Q(first_name=name) | Q(email=name) | Q(last_name=name)).all(
            ) if request.user.is_authenticated else [])
            return render(request, self.template_name, {"contacts": contacts, "form": form})
        else:
            form = SearchContactNameForm()
            return render(request, "contacts/error.html", {"message": "Something went wrong"})


# from Django documentation
# b = Blog.objects.get(pk=1)
# # This will delete the Blog and all of its Entry objects.
# b.delete()


# @method_decorator(login_required, name="dispatch")
# class contact_list(View):
#     template_name = "contacts/contact_list.html"

#     def get(self, request, *args, **kwargs):
#         contacts = (
#             Contact.objects.filter(user=request.user).all()
#             if request.user.is_authenticated
#             else []
#         )
#         return render(request, self.template_name, {"contacts": contacts})
