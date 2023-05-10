from django.db import models
from django.core.validators import RegexValidator


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        )
    text = models.TextField(
        verbose_name='Описание',
        max_length=5000,
        )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        default=1,
        )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет в "HEX"',
        max_length=7,
        unique=True,
    )
    slug = models.CharField(
        verbose_name='Уникальный фрагмент URL-адреса',
        max_length=200,
        validators=([RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')])
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)