from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('db_backup_schedule', DbBackupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('backup_db/',DbBackupApi.as_view()),

]