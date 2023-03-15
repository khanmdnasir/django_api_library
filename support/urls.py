from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('issue-types',IssueTypesViewSet),
urlpatterns=[
    path('', include(router.urls)),
    # path("email-test/",EmailTest.as_view(),name="email_test"),
]
