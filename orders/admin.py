from django.contrib import admin
from django.urls import path
from . import views
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('sequence_number', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sequence_number__startswith', 'user__username__startswith')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(views.order_management_view), name='orders_order_changelist'),
        ]
        # Возвращаем кастомный URL первым, чтобы он имел приоритет над стандартным URL списка
        return custom_urls + urls


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'dish', 'quantity', 'price', 'total_price')
    # Добавляем total_price как метод класса для отображения в админке
    def total_price(self, obj):
        # Убедитесь, что price и quantity не равны None перед умножением
        price = obj.price if obj.price is not None else 0
        quantity = obj.quantity if obj.quantity is not None else 0
        return f"{price * quantity} ₽"
    total_price.short_description = 'Общая стоимость' # Название столбца в админке


# Регистрируем модели с классами Admin
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)