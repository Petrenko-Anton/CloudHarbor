import os
import dropbox
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import FileForm
from .models import File
from .utils import get_file_category, get_file_size
from django.contrib.auth.decorators import login_required


# ключ API тимчасово тут
dbx = dropbox.Dropbox(settings.DROP_BOX)



# Функція завантаження файлів
# def upload(request):
#     form = FileForm(instance=File())
#     if request.method == 'POST':
#         form = FileForm(request.POST, request.FILES, instance=File())
#         if form.is_valid():
#             file = form.save()
@login_required()
def upload(request):
    form = FileForm(instance=File())
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES, instance=File())
        if form.is_valid():
            file = form.save(commit=False)
            if file.path:
                # Отримуємо категорію за допомогою get_file_category
                category = get_file_category(file.path.name)
                file.category = category
                # Зберігаємо файл
                file.save()
            # Шлях до файлу на Dropbox та локального файлу
            dropbox_path = f'/uploads/{file.path.name}'
            local_path = os.path.join(settings.MEDIA_ROOT, file.path.name)
            size = get_file_size(local_path)
            file.size = size
            file.save()
            # Завантаження файла на Dropbox
            with open(local_path, 'rb') as f:
                dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode('overwrite'))

            return redirect(to="files:files")
    return render(request, 'files/upload.html', context={"title": "Files", "form": form})


# Функція відображення файлів
def files(request):
    files_ = (
        File.objects.filter(user=request.user).all()
        if request.user.is_authenticated
        else []
    )
    return render(request, 'files/files.html', context={"title": "Files", "files": files_, "media": settings.MEDIA_ROOT})


# Функція видалення файлів
@login_required()
def remove(request, file_id):
    file = File.objects.filter(pk=file_id)
    try:
        os.unlink(os.path.join(settings.MEDIA_ROOT, str(file.first().path)))
    except OSError as e:
        print(e)
    file.delete()
    return redirect(to='files:files')


# Функція редагування файлів
@login_required()
def edit(request, file_id):
    if request.method == 'POST':
        description = request.POST.get('description')
        category = request.POST.get('category')
        File.objects.filter(pk=file_id).update(description=description, category=category)
        return redirect(to='files:files')

    file = File.objects.filter(pk=file_id).first()
    return render(request, "files/edit.html",
                  context={"title": "Files", "file": file, "media": settings.MEDIA_ROOT})
