from django.db import models
from django.core.validators import RegexValidator
from users.models import CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор',
        related_name='recipes',
        on_delete=models.CASCADE,
        default=1
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
        help_text='Загрузите изображение',
        null=True,
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=5000,
        )
    ingredient = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='IngredientAmount'
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

    def __str__(self):
        return self.name


class Ingredient(models.Model):
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


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class Subscriptions(models.Model):
    user = models.ForeignKey(
        'CustomUser',
        verbose_name='Подписчик',
        related_name='subscriber',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        'CustomUser',
        verbose_name='Автор',
        related_name='subscribing',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(fields=('user', 'author'), name='unique_subscriptions')
        )

    def __str__(self) -> str:
        return f'{self.user} подписан(-а) на {self.author}'