from django.db import models
from django.core.validators import RegexValidator
from users.models import CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
        help_text='Загрузите изображение',
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=5000,
        )
    tag = models.ManyToManyField(
        'Tag',
        verbose_name='Тег',
        related_name='recipes',
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
        ordering = ('-pub_date',)

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


class Ingridient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)