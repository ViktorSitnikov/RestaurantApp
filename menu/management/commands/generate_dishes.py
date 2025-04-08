# your_app/management/commands/generate_dishes.py
from django.core.management.base import BaseCommand
from faker import Faker
from menu.models import Category, Dishes  # Замените your_app на имя вашего приложения
import random


class Command(BaseCommand):
    help = 'Генерация тестовых блюд в базу данных'

    def handle(self, *args, **options):
        fake = Faker('ru_RU')

        # # Создаем категории если их нет
        # categories = ['Горячее', 'Роллы', 'Супы', 'Салаты', 'Десерты', 'Напитки']
        # for cat in categories:
        #     Category.objects.get_or_create(name=cat)

        # Списки для генерации правдоподобных названий
        dish_types = ['ролл', 'суши', 'салат', 'суп', 'десерт', 'напиток']
        adjectives = ['Спайси', 'Острый', 'Нежный', 'Фирменный', 'Императорский']
        ingredients = ['лососем', 'тунцом', 'угрем', 'креветкой', 'авокадо', 'сыром']

        photolink = ['Карбонара', 'Кофе', 'Роллы']

        # Генерация 20 тестовых блюд
        for _ in range(40):
            dish_name = f"{random.choice(adjectives)} {random.choice(ingredients)} {random.choice(dish_types)}"

            Dishes.objects.create(
                name=dish_name,
                price=random.randint(150, 1500),
                description=fake.text(max_nb_chars=200),
                photolink=f"{random.choice(photolink)}",
                rate=round(random.uniform(3.5, 5.0), 1),
                grams=f"{random.randint(50, 500)}",
                kalories=random.randint(50, 800),
                protein=round(random.uniform(1, 30), 1),
                fat=round(random.uniform(1, 25), 1),
                carbohydrates=round(random.uniform(5, 100), 1),
                structure=", ".join([fake.word() for _ in range(5)]),
                is_available=random.choice([True, False]),
                is_new=random.choice([True, False]),
                is_hit=random.choice([True, False]),
                category=random.choice(Category.objects.all())
            )

        self.stdout.write(self.style.SUCCESS('Успешно создано 20 тестовых блюд'))