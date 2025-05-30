from django.db import models, transaction
from menu.models import Dishes
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Order(models.Model):
    MAX_ORDER_NUMBER = 500  # Максимальный номер заказа
    STATUS_CHOICES = [
        ('Готовится', 'Готовится'),
        ('Выполнен', 'Выполнен'),
        ('Завершён', 'Завершён'),
        ('Отменен', 'Отменен'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_rated = models.BooleanField(default=False)
    
    sequence_number = models.PositiveIntegerField(
        editable=False,
        db_index=True,
        default=1
    )
    
    class Meta:
        ordering = ['sequence_number']

    @classmethod
    def get_next_sequence_number(cls):
        with transaction.atomic():
            # Блокируем таблицу для предотвращения гонки
            last_order = cls.objects.select_for_update().order_by('-sequence_number').first()
            
            if last_order:
                next_num = last_order.sequence_number + 1
                if next_num > cls.MAX_ORDER_NUMBER:
                    next_num = 1
            else:
                next_num = 1
                
            return next_num

    def save(self, *args, **kwargs):
        if not self.sequence_number:
            self.sequence_number = self.get_next_sequence_number()
        super().save(*args, **kwargs)
    
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Готовится')

    def __str__(self):
        return f"Заказ {self.id} от {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.OneToOneField(
        'DishRating',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rated_order_item'  
    )

    def __str__(self):
        return f"Товар {self.dish.name} в количестве {self.quantity} шт."
    
class DishRating(models.Model):
    dish = models.ForeignKey(Dishes, on_delete=models.CASCADE, related_name='dish_ratings')
    order_item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
