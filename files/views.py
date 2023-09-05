import os
import dropbox
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .forms import FileForm
from .models import File

# ключ API тимчасово тут
dbx = dropbox.Dropbox(
    'sl.Ble2pGJmXbmTWPPYdl1AmVvqVUJd1g3_rv7tYcFK456vm_p5TkyMnsGIMe2LmMobqfWvtJfea3csmzVsJv8PT2haVhD9TSnuUonW3oZ5cjA76jfgGXmQYWdsbEUlNqX5g-S9RRPGwes9')


def main(request):
    return render(request, 'contacts/index.html', context={"title": "Files"})

# @csrf_exempt
# def upload(request):
#     if request.method == 'POST' and request.FILES.get('file'):
#         uploaded_file = request.FILES['file']
#         file_name = uploaded_file.name
#         dropbox_path = f'/uploads/{file_name}'  # Вкажіть шлях на Dropbox, де потрібно зберегти файл
#
#         try:
#             with uploaded_file.open() as file:
#                 dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode('overwrite'))
#             return JsonResponse({'message': 'File uploaded successfully'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#
#     return JsonResponse({'error': 'Invalid request'}, status=400)
#
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
