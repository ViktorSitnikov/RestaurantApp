from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    icon_class = models.CharField(max_length=100, default="123", verbose_name="Класс иконки font-awesome")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/Category/{self.id}'

class Dishes(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(blank=True, verbose_name="Описание")
    photolink = models.CharField(max_length=255, verbose_name="Фотография")
    rate = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)],  verbose_name="Рейтинг")
    grams = models.CharField(max_length=50, verbose_name="Граммы")
    kalories = models.DecimalField(max_digits=6, decimal_places=1, verbose_name="Калории")
    protein = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Белки")
    fat = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Жиры")
    carbohydrates = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Углеводы")
    structure = models.CharField(max_length=255, verbose_name="Состав")
    is_available = models.BooleanField(default=False, verbose_name="Доступен для заказа")
    is_new = models.BooleanField(default=False, verbose_name="Новое")
    is_hit = models.BooleanField(default=False, verbose_name="Хит")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="products")

    def __str__(self):
        return self.name


