# Generated by Django 4.2.1 on 2023-05-15 14:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_favorites_shoppingcart_subscriptions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='default.jpg', help_text='Загрузите изображение', upload_to='recipes/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator(regex='^#[A-Fa-f0-9]{6}$')], verbose_name='Цвет в "HEX"'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator(regex='^[-a-zA-Z0-9_]+$')], verbose_name='Уникальный фрагмент URL-адреса'),
        ),
    ]
