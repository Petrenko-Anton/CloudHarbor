import datetime
import json
import mimetypes
import os

import dropbox
import requests
from allauth.socialaccount.providers.oauth.client import OAuthError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import FileForm
from .models import File
from .utils import get_file_category, get_file_size

# dbx = dropbox.Dropbox(settings.DROP_BOX)

DROPBOX_APP_KEY = settings.DROPBOX_APP_KEY
DROPBOX_APP_SECRET = settings.DROPBOX_APP_SECRET
REDIRECT_URL = 'http://127.0.0.1:8000/files/'


def dropbox_oauth(request):
    print('Auth Started !!!!!!!!!!!')
    return redirect(
        f'https://www.dropbox.com/oauth2/authorize?client_id={DROPBOX_APP_KEY}&redirect_uri={REDIRECT_URL}authorized&response_type=code')


def dropbox_authorized(request):
    try:
        code = request.GET["code"]
        print(f"Code: {code}")
    except KeyError:
        return JsonResponse({"error": "Authorization code not found in the request."}, status=400)
    data = requests.post('https://api.dropboxapi.com/oauth2/token', {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": f"{REDIRECT_URL}authorized",
        "client_id": DROPBOX_APP_KEY,
        "client_secret": DROPBOX_APP_SECRET})
    request.session["DROPBOX_ACCESS_TOKEN"] = data.json()["access_token"]
    with open('OAuth_token.json', 'w') as file:
        json.dump(
            {"datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "token": data.json()["access_token"]},
            file, indent=4, ensure_ascii=False)

    return redirect(to="files:files")


def get_access_token():
    with open('OAuth_token.json', 'r') as file:
        data = json.load(file)
        date = data.get('datetime')
        date_dt_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        current_time = datetime.datetime.now()
        delta_hours = ((current_time - date_dt_obj).total_seconds()) / 60 / 60
        print(delta_hours)
        if delta_hours > 3:
            return None
        token = data.get('token')
        print(date, token)
        return token


def get_access_dbx(request):
    dbx = None
    try:
        access_token = get_access_token()
        if access_token:
            dbx = dropbox.Dropbox(access_token)
        else:
            print("Try refresh!")
            return redirect(to="files:dropbox_oauth")
    except Exception as err:
        print(f"My ERROR ! : {err}")

    return dbx

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
                file.user = request.user
                file.save()
            # Шлях до файлу на Dropbox та локального файлу
            dropbox_path = f'/uploads/{file.path.name}'
            local_path = os.path.join(settings.MEDIA_ROOT, file.path.name)
            size = get_file_size(local_path)
            file.size = size
            file.dropbox_path = dropbox_path
            file.save()
            # Завантаження файла на Dropbox
            dbx = get_access_dbx(request)
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
    return render(request, 'files/files.html', context={"title": "Files", "files": files_})


# Функція видалення файлів
@login_required()
def remove(request, file_id):
    dbx = get_access_dbx(request)
    file = File.objects.filter(pk=file_id).first()
    print(file_id, file.dropbox_path)
    try:
        os.unlink(os.path.join(settings.MEDIA_ROOT, str(file.path)))
    except OSError as e:
        print(e)
    try:
        dbx.files_delete_v2(file.dropbox_path)
        file.delete()

    except OAuthError as e:
        print(e)
    return redirect(to='files:files')


# скачування фвйлів
@login_required()
def download(request, file_id):
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'INSTANCE ::::::::::::::: {dbx}')
        return redirect(to='files:dropbox_oauth')

    file = File.objects.filter(pk=file_id).first()

    dbx.files_download_to_file(os.path.join(settings.MEDIA_ROOT, file.orig_name), file.dropbox_path)
    local_path = os.path.join(settings.MEDIA_ROOT, file.orig_name)

    content_type, _ = mimetypes.guess_type(local_path)
    if content_type is None:
        content_type = 'application/octet-stream'

    response = FileResponse(open(local_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file.orig_name}"'
    return response


# відображення файлів
@login_required()
def show(request, file_id):
    dbx = get_access_dbx(request)
    if isinstance(dbx, (HttpResponseRedirect, type(None))):
        print(f'INSTANCE ::::::::::::::: {dbx}')
        return redirect(to='files:dropbox_oauth')

    file = File.objects.filter(pk=file_id).first()
    if file.orig_name.split('.')[1] not in ('html', 'htm', 'txt', 'xml', 'json', 'svg', 'jpg', 'jpeg', 'png,' 'gif',
                                            'bmp', 'css', 'js', 'webm', 'pdf', 'mp3', 'wav'):
        return redirect(to="files:files")
    dbx.files_download_to_file(os.path.join(settings.MEDIA_ROOT, file.orig_name), file.dropbox_path)
    local_path = os.path.join(settings.MEDIA_ROOT, file.orig_name)

    response = FileResponse(open(local_path, 'rb'))
    return response


# Функція редагування файлів
@login_required()
def edit(request, file_id):
    if request.method == 'POST':
        description = request.POST.get('description')
        File.objects.filter(pk=file_id).first().update(description=description)
        return redirect(to='files:files')

    file = File.objects.filter(pk=file_id).first()
    return render(request, "files/edit.html",
                  context={"title": "Files", "file": file})

# Функція перегляду інфо про файл
def detail(request, file_id):
    if request.method == 'GET':
        description = request.GET.get('description')
        category = request.GET.get('category')

    file = File.objects.filter(pk=file_id).first()
    return render(request, "files/detail.html",
                  context={"title": "Files", "file": file})
