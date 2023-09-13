import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

from .forms import ContactForm, SearchContactNameForm, SearchContactEmailForm
from .models import Contact


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
    template_name = "contacts/birthlist.html"
    week_offset = 7
    
    def post(self, request, *args, **kwargs):
        week_offset = request.POST.get('week_offset')
        try:
            week_offset = int(week_offset)
            if week_offset < 1:  # Перевірка на додатнє значення
                raise ValueError()
        except (ValueError, TypeError):
            week_offset = 7  # Встановлення значення за замовчуванням
            messages.error(request, "Введіть коректне число більше 0.")
        
        self.week_offset = week_offset
        return self.get(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        week_offset = self.week_offset
        today_date = datetime.date.today()
        day_in_a_week = today_date + datetime.timedelta(days=self.week_offset)
        month = day_in_a_week.month
        day = day_in_a_week.day
        contacts = (
            Contact.objects.filter(user=request.user).all()
            if request.user.is_authenticated
            else []
        )

        aniversaire_contacts = []
        for contact in contacts:
            if today_date.day <= contact.birth_date.day <= day and contact.birth_date.month == month:
                aniversaire_contacts.append(contact)

        return render(request, self.template_name, {"contacts": aniversaire_contacts})


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

    def get(self, request, contact_id):
        contact = Contact.objects.get(pk=contact_id)
        return render(request, self.template_name, {"contact": contact})


@method_decorator(login_required, name="dispatch")
class edit_contact(View):
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


@method_decorator(login_required, name="dispatch")
class delete_contact(View):
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
class contact_search_by_email(View):
    template_name = "contacts/contacts.html"

    def get(self, request, *args, **kwargs):
        form = SearchContactEmailForm()
        return render(request, "contacts/contact_search_by_email.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SearchContactEmailForm(request.POST)
        if form.is_valid():
            search_email = form.cleaned_data["search_email"]
            contacts = (Contact.objects.filter(user=request.user, email=search_email).all(
            ) if request.user.is_authenticated else [])
            return render(request, self.template_name, {"contacts": contacts})
        else:
            form = SearchContactEmailForm()
            return render(request, "contacts/contact_search_by_email.html", {"form": form})


@method_decorator(login_required, name="dispatch")
class contact_search_by_name(View):
    template_name = "contacts/contacts.html"

    def get(self, request, *args, **kwargs):

        form = SearchContactNameForm()
        return render(request, "contacts/contact_search_by_name.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = SearchContactNameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["search_name"]
            contacts = (Contact.objects.filter(user=request.user, first_name=name).all(

            ) if request.user.is_authenticated else [])
            return render(request, self.template_name, {"contacts": contacts, "form": form})
        else:
            form = SearchContactNameForm()

            return render(request, "contacts/contact_search_by_name.html", {"form": form})