import os
import dropbox
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FileForm
from .models import File

# ключ API тимчасово тут
dbx = dropbox.Dropbox(
    'sl.BlWbv8sLr9A-txbOBOchHrlqg3Sqd4zRb6wEt8XdPu70Kp_IN9M99QDam87w-GrEz9VcGyeexKcRc_PX7KXds0agbFqhSdZrQGHkmxtBYitR1Y5ZRAHz3e574EiiuRf4X81kDzUpzS3J')


def main(request):
    return render(request, 'contacts/index.html', context={"title": "Files"})


# Функція завантаження файлів
def upload(request):
    form = FileForm(instance=File())
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=File())
        if form.is_valid():
            file = form.save()

            # Шлях до файлу на Dropbox та локального файлу
            dropbox_path = f'/uploads/{file.path.name}'
            local_path = os.path.join(settings.MEDIA_ROOT, file.path.name)

            # Завантаження файла на Dropbox
            with open(local_path, 'rb') as f:
                dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode('overwrite'))

            return redirect(to="files:files")
    return render(request, 'files/upload.html', context={"title": "Files", "form": form})


# Функція відображення файлів
def files(request):
    file = File.objects.all()
    return render(request, 'files/files.html', context={"title": "Files", "files": file, "media": settings.MEDIA_URL})


# Функція видалення файлів
def remove(request, file_id):
    file = File.objects.filter(pk=file_id)
    try:
        os.unlink(os.path.join(settings.MEDIA_ROOT, str(file.first().path)))
    except OSError as e:
        print(e)
    file.delete()
    return redirect(to='files:files')


# Функція редагування файлів
def edit(request, file_id):
    if request.method == 'POST':
        description = request.POST.get('description')
        category = request.POST.get('category')
        File.objects.filter(pk=file_id).update(description=description, category=category)
        return redirect(to='files:files')

    file = File.objects.filter(pk=file_id).first()
    return render(request, "files/edit.html",
                  context={"title": "Files", "file": file, "media": settings.MEDIA_URL})
