from .views import *
from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter()
router.register('payment-gateway',PaymentGatewayViewSet)
router.register('currency',CurrencyViewset)

urlpatterns = [
    path('payment/',PaymentView.as_view()),
    path('payment-subscription/',PaymentSubscriptionView.as_view()),
    path('stripe_config/',StripeConfigView.as_view()),
]