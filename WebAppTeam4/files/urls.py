from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "files"

urlpatterns = [
    path('authorize/', views.dropbox_oauth, name='dropbox_oauth'),
    path('authorized/', views.dropbox_authorized, name='dropbox_authorized'),
    path('', views.files, name='files'),
    path('upload/', views.upload, name='upload'),
    path('view/<int:file_id>', views.detail, name='detail'),
    path('edit/<int:file_id>', views.edit, name='edit'),
    path('remove/<int:file_id>', views.remove, name='remove'),
    path('download/<int:file_id>', views.download, name='download'),
    path('show/<int:file_id>', views.show, name='show')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)