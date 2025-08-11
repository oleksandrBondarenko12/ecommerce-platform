from django.urls import path
from .views import MockPaymentView


urlpatterns = [
    path('mock-pay/', MockPaymentView.as_view(), name='mock-payment'),
]

