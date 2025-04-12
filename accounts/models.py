from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=100, verbose_name="Название роли")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/Role/{self.id}'

class Users(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество")
    email = models.EmailField(max_length=255, verbose_name="Почта")
    phone_number = models.CharField(max_length=11, verbose_name="Телефон")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Роль", related_name="users")
    photo = models.ImageField(upload_to='cars')

    def __str__(self):
        return self.name



