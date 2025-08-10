# In cart/models.py
from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    # A cart should belong to one user, and a user should only have one cart.
    # OneToOneField is the perfect choice for this relationship.
    # Using settings.AUTH_USER_MODEL makes the app compatible with custom user models.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    # An item belongs to a cart. If a cart is deleted, its items should be too.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    # An item is a specific product. If the product is deleted, remove it from all carts.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"
