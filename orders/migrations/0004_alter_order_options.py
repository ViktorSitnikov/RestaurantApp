# Generated by Django 5.2 on 2025-05-21 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_is_rated_alter_order_sequence_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-created_at']},
        ),
    ]
