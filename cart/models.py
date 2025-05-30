from django.db import models
from menu.models import Dishes
from accounts.models import CustomUser

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Для неавторизованных пользователей
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Корзина для {self.user.username}"
        return f"Корзина для гостя с сессией {self.session_key}"

    def save(self, *args, **kwargs):
        if not self.user and not self.session_key:
            self.session_key = self.session_key or ''
        super(Cart, self).save(*args, **kwargs)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dishes = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.dishes.name} x{self.quantity}"

    def get_cost(self):
        return self.dishes.price
    
    @property
    def price(self):
        return self.dish.price * self.quantity 
