# CloudHarbor

Personal Assistant web application \
(localized Ukrainian version)

# Main Features

* CONTACT BOOK
    * addition
    * edit
    * remove
    * search by name or by email
    * nearest birthdays
* NOTES
    * searchable tags
    * creation date
    * finished /done checkinng
* CLOUD FILE STORAGE
    * upload your files with comments
    * pics, audio and documents can be viewed / payed
    * automatic category detection
    * filtering by categories
* NEWS (localized)
    * 7 topics of fresh news
    * currency exchange rates
    * current weather, main Ukrainian cities
    * weather forecast (redirect)

# Installation to Local Machine

* Must have Python 3.11 installed
* clone this repository to your PC
* poetry environment manager - create environment
* create .env file using included env.example.txt file

# First start of the app

* for creating dropbox variables you need to create app in dropbox and get access token:

    * https://www.dropbox.com/developers/apps
    * in your app give permissions for read and write
    * add to .env DROPBOX_APP_KEY=APPKEYHERE
    * add to .env DROPBOX_APP_SECRET=APPSECRETHERE
      by this link you can get access token, only replace APPKEYHERE with your app key
    * https://www.dropbox.com/oauth2/authorize?client_id=APPKEYHERE&response_type=code&token_access_type=offline
* python manage.py makemigrations - create migrations
* python manage.py migrate - applying migrations
* python manage.py createsuperuser - create superuser
* python manage.py runserver - start app

# All th next stats

* python manage.py runserver - start app

# USAGE

go to http://localhost:8000/
  

  