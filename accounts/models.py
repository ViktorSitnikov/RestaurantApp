from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    # Добавляем уникальные related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",  # Уникальное имя
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",  # Уникальное имя
        related_query_name="user",
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Принудительно устанавливаем is_active=True для новых пользователей
        if not self.pk:  # Если это новый пользователь
            self.is_active = True
        super().save(*args, **kwargs)