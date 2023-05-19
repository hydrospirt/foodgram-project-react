from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from recipes.models import (Favorites, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Subscriptions, Tag)

User = get_user_model()


class TagModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tag = Tag.objects.create(
            name='Тест',
            color='#fffafa',
            slug='test',
        )

    def test_verbose_name(self):
        """verbose_name всех полей модели "Tag" совпадает с ожидаемым."""
        tag = TagModelTest.tag
        field_verboses = {
            'name': 'Название',
            'color': 'Цвет в виде "HEX"',
            'slug': 'Уникальный фрагмент URL-адреса',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    tag._meta.get_field(value).verbose_name, expected
                )


class IngredientModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ingredient = Ingredient.objects.create(
            name='Тест',
            measurement_unit='кг'
        )

    def test_verbose_name(self):
        """verbose_name всех полей модели "Ingredient" совпадает с ожидаемым."""
        ingredient = IngredientModelTest.ingredient
        field_verboses = {
            'name': 'Название',
            'measurement_unit': 'Единица измерения',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    ingredient._meta.get_field(value).verbose_name, expected
                )


class RecipeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='testauthor')
        cls.ingredient = Ingredient.objects.create(
            name='Соль',
            measurement_unit='г',)
        cls.tag = Tag.objects.create(
            name='Супер',
            color='#feee00',
            slug='mytest',)
        cls.recipe = Recipe.objects.create(
            author=cls.author,
            name='Тестовый рецепт',
            text='Тестовое описание',
            cooking_time=30,
            pub_date=datetime.now()
        )
        cls.amount = IngredientAmount.objects.create(
            recipe=cls.recipe,
            ingredient=cls.ingredient,
            amount=100,
        )

    def test_verbose_name(self):
        """verbose_name всех полей модели "Recipe" совпадает с ожидаемым."""
        recipe = RecipeModelTest.recipe
        field_verboses = {
            'author': 'Автор',
            'name': 'Название',
            'image': 'Картинка',
            'text': 'Описание',
            'ingredient': 'Ингредиенты',
            'tag': 'Теги',
            'cooking_time': 'Время приготовления',
            'pub_date': 'Дата публикации',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    recipe._meta.get_field(value).verbose_name, expected
                )


class FavoritesModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='testfav')
        cls.recipe = Recipe.objects.create(
            name='Тестовый рецепт',
            text='Тестовое описание',
            cooking_time=30,
            pub_date=datetime.now()
        )
        cls.favorite = Favorites.objects.create(
            user=cls.user, recipe=cls.recipe
        )

    def test_verbose_name(self):
        """verbose_name всех полей модели "Favorites" совпадает с ожидаемым."""
        fav = FavoritesModelTest.favorite
        field_verboses = {
            'user': 'Пользователь',
            'recipe': 'Рецепт'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    fav._meta.get_field(value).verbose_name, expected
                )


class IngredientAmountModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='testauthor')
        cls.ingredient = Ingredient.objects.create(
            name='Сахар',
            measurement_unit='г',)
        cls.recipe = Recipe.objects.create(
            author=cls.author,
            name='Тестовый рецепт',
            text='Тестовое описание',
            cooking_time=30,
            pub_date=datetime.now()
        )
        cls.amount = IngredientAmount.objects.create(
            recipe=cls.recipe,
            ingredient=cls.ingredient,
            amount=100,
        )

    def test_verbose_name(self):
        """verbose_name всех полей модели "IngredientAmount" совпадает с ожидаемым."""
        amount = IngredientAmountModelTest.amount
        field_verboses = {
            'recipe': 'Рецепт',
            'ingredient': 'Ингредиент',
            'amount': 'Количество',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    amount._meta.get_field(value).verbose_name, expected
                )


# class ShoppingCartModelTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user = User.objects.create(username='shoptestuser')
#         cls.author = User.objects.create(username='testshopauthor')
#         cls.recipe = Recipe.objects.create(
#             author=cls.author,
#             name='Тестовый рецепт',
#             text='Тестовое описание',
#             cooking_time=600,
#             pub_date=datetime.now()
#         )
#         cls.shop_cart = ShoppingCart.objects.create(
#             user=cls.user, recipe=cls.recipe
#         )


#     def test_verbose_name(self):
#         shop_cart = ShoppingCartModelTest.shop_cart
#         field_verboses = {
#             'user': 'Покупатель',
#             'recipe': 'Рецепт'
#         }
#         for value, expected in field_verboses.items():
#             with self.subTest(value=value):
#                 self.assertEqual(
#                     shop_cart._meta.get_field(value).verbose_name, expected
#                 )

# class SubscriptionsModelTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.subscriber = User.objects.create(username='testusersub')
#         cls.author = User.objects.create(username='testsubauthor')
#         cls.subscriptions = Subscriptions.objects.create(
#             user=cls.subscriber,
#             author=cls.author,
#         )

#     def test_verbose_name(self):
#         """verbose_name всех полей модели "Subscriptions" совпадает с ожидаемым."""
#         sub = SubscriptionsModelTest.subscriptions
#         field_verboses = {
#             'user': 'Подписчик',
#             'author': 'Автор'
#         }
#         for value, expected in field_verboses.items():
#             with self.subTest(value=value):
#                 self.assertEqual(
#                     sub._meta.get_field(value).verbose_name, expected
#                 )
