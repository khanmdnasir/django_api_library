from django.apps import AppConfig


class ActivitylogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'activityLog'

    def ready(self):
        from . import receivers


    