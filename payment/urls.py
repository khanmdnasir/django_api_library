from .views import *
from django.urls import path
from rest_framework import routers


router = routers.DefaultRouter()
router.register('payment',PaymentGatewayViewSet)
router.register('currency',CurrencyViewset)

urlpatterns = [
    path('test-payment/',test_payment.as_view()),
    path('stripe-payment/',StripePaymentView.as_view()),
    path('stripe-payment-subscription/',StripePaymentSubscriptionView.as_view()),
]