from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('issue-types',IssueTypesViewSet),
router.register('ticket',TicketViewSet),
router.register('ticket-comments',TicketCommentsViewSet),
router.register('ticket-logs',TicketLogsViewSet),
urlpatterns=[
    path('', include(router.urls)),
    path("close-ticket/",CloseOrOpenTicketApi.as_view(),name="close-ticket"),
]
