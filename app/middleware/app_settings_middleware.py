from django.conf import settings
from ..models import AppSettings

# Create your views here.


class AppSettingsMiddleware(object):
    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            appSettings = AppSettings.objects.get()
            print('before middleware',settings.DEFAULT_FILE_STORAGE)
            if appSettings.storage_used == 'aws':
                settings.DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        except AttributeError:
            pass
        return None