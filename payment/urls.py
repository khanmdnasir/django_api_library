from .views import *
from django.urls import path,include
from rest_framework import routers


router = routers.DefaultRouter()
router.register('payment-gateway',PaymentGatewayViewSet)
router.register('currency',CurrencyViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('payment/',PaymentView.as_view()),
    path('payment_receive/',PaymentReceiveView.as_view())
]