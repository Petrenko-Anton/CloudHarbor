from django.urls import path
from . import views

app_name = "files"

urlpatterns = [
    path('', views.main, name='root'),
    path('upload/', views.upload, name='upload'),
    path('files/', views.files, name='files'),
    path('files/edit/<int:file_id>', views.edit, name='edit'),
    path('files/remove/<int:file_id>', views.remove, name='remove'),
]
