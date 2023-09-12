from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("notes/", views.main, name="main"),
    path("tag/", views.tag, name="tag"),
    path("note/", views.note, name="note"),
    path("detail/<int:note_id>", views.detail, name="detail"),
    path("done/<int:note_id>", views.set_done, name="set_done"),
    path("delete/<int:note_id>", views.delete_note, name="delete"),
    path("edit_note/<int:note_id>", views.edit_note, name="edit_note"),
    path("search_my_name", views.search_by_name, name="search_by_name"),
    path("note_search_page", views.note_search_page, name="note_search_page"),
    path("tags/", views.tags_page, name="tags_page"),
    path("tags/<int:tag_id>", views.tagnotes, name="tagnotes"),
]
