from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, NoteForm, SearchNoteForm
from .models import Tag, Note
from django.contrib.auth.decorators import login_required


# Create your views here.
def main(request):
    notes = (
        Note.objects.filter(user=request.user).all()
        if request.user.is_authenticated
        else []
    )
    return render(request, "notes/notes.html", {"notes": notes})


@login_required
def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to="notes:main")
        else:
            return render(request, "notes/tag.html", {"form": form})

    return render(request, "notes/tag.html", {"form": TagForm()})


@login_required
def note(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist("tags"), user=request.user
            )
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to="notes:main")
        else:
            return render(request, "notes/note.html", {"tags": tags, "form": form})

    return render(request, "notes/note.html", {"tags": tags, "form": NoteForm()})


@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, "notes/detail.html", {"note": note})


@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to="notes:main")


@login_required
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to="notes:main")


@login_required
def edit_note(request, note_id):
    tags = Tag.objects.filter(user=request.user).all()
    if request.method == "POST":
        form = NoteForm(request.POST)
        note = Note.objects.get(pk=note_id)
        if form.is_valid():
            updated_note = form.save(commit=False)
            updated_note.user = request.user

            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist("tags"), user=request.user
            )

            for tag in note.tags.iterator():
                note.tags.remove(tag)

            for tag in choice_tags.iterator():
                note.tags.add(tag)

            Note.objects.filter(pk=note_id).update(name=updated_note.name,
                                                   description=updated_note.description,
                                                   )

            return redirect(to="notes:main")
        else:
            return render(request, "notes/editnote.html", {"note": note, "form": form})

    note = Note.objects.get(pk=note_id)
    default_settings = {
        "name": note.name,
        "description": note.description,
    }
    form = NoteForm(initial=default_settings)
    return render(request, "notes/editnote.html", {"tags": tags, "form": form, "note": note})


def search_by_name(request):
    if request.method == "GET":
        form = SearchNoteForm(request.GET)
        if form.is_valid():
            search_name = form.cleaned_data["search_name"]
            notes = (
                Note.objects.filter(user=request.user, name=search_name).all()
                if request.user.is_authenticated
                else []
            )
            return render(request, "notes/notes.html", {"notes": notes})


def note_search_page(request):
    form = SearchNoteForm()
    return render(request, "notes/note_search_by_name.html", {"form": form})
