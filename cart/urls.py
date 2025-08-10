# In cart/urls.py
from django.urls import path
from .views import CartView

urlpatterns = [
    # This single URL will handle GET, POST, and DELETE for the user's cart.
    path('', CartView.as_view(), name='cart-detail'),
]
