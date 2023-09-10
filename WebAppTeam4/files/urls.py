from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "files"

urlpatterns = [
    path('', views.main, name='root'),
    path('upload/', views.upload, name='upload'),
    path('files/', views.files, name='files'),
    path('files/edit/<int:file_id>', views.edit, name='edit'),
    path('files/remove/<int:file_id>', views.remove, name='remove'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)