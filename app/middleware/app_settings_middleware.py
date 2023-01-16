from django.conf import settings
from ..models import AppSettings

# Create your views here.


class AppSettingsMiddleware(object):
    def __init__(self, get_response):
            self.get_response = get_response

    def __call__(self, request):
        appSettings = AppSettings.objects.get()
        print('app settings call',appSettings.debug)
        return self.get_response(request)
    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            appSettings = AppSettings.objects.get()
            print('app settings',appSettings.debug)
            settings.storage_used = appSettings.storage_used
        except AttributeError:
            pass
        return None