from django.apps import AppConfig


class FilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'files'

    def ready(self):
        # Імпортуйте ваші крон-завдання тут і зареєструйте їх
        from files.cron import MyCronJob  # Замініть `myapp` на назву вашого додатку

        # Зареєструйте ваше крон-завдання
        MyCronJob()
