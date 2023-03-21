from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('menu', MenuViewSet)
router.register('sub_menu', SubMenuViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('sub_menu_by_menu/',SubMenuApi.as_view()),

]