from collections import OrderedDict
from datetime import datetime
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from recipes.models import (Ingredient, IngredientAmount, Recipe, ShoppingCart,
                            Tag)
from rest_framework.test import APIClient

User = get_user_model()


class ApiURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest = Client()
        cls.user = User.objects.create_user(id=1, username='testman',
                                            email='tester@test.ru')
        cls.author = User.objects.create_user(username='testauthor',
                                              email='author@test.ru',
                                              first_name='ИмяТест',
                                              last_name='ФамилияТест',
                                              password='Efdfs13131')
        cls.tag = Tag.objects.create(
            name='Тест',
            color='#fffafa',
            slug='test',
        )
        cls.ingredient = Ingredient.objects.create(
            name='Тестовый ингредиент',
            measurement_unit='г'
        )
        cls.recipe = Recipe.objects.create(
            author=cls.author,
            name='Тестовый рецепт',
            text='Тестовое описание',
            cooking_time=30,
            pub_date=datetime.now()
        )
        cls.recipe_second = Recipe.objects.create(
            author=cls.author,
            name='Тестовый рецепт второй',
            text='Тестовое описание',
            cooking_time=35,
            pub_date=datetime.now()
        )

        cls.amount = IngredientAmount.objects.create(
            recipe=cls.recipe,
            ingredient=cls.ingredient,
            amount=100
        )
        cls.shopping_cart = ShoppingCart.objects.create(
            user=cls.user,
            recipe=cls.recipe
        )
        cls.recipe.ingredient.add(cls.ingredient)
        cls.recipe.tags.add(cls.tag)

    def setUp(self):
        self.auth_follower = APIClient()
        self.auth_follower.force_authenticate(self.user)
        self.auth_author = APIClient()
        self.auth_author.force_authenticate(self.author)

    def test_api_guest_urls(self):
        pages = (
            '/api/users/',
            '/api/tags/',
            f'/api/tags/{self.tag.pk}/',
            '/api/recipes/',
            f'/api/recipes/{self.recipe.pk}/',
            '/api/ingredients/',
            f'/api/ingredients/{self.ingredient.pk}/'
        )
        for page in pages:
            with self.subTest(page=page):
                response = self.guest.get(page)
                error_msg = ('Ошибка: у не авторизованного пользователя',
                             f'нет доступа к странице {page}')
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    error_msg
                )

    def test_auth_author_urls(self):
        pages = (
            '/api/users/',
            f'/api/users/{self.author.pk}/',
            '/api/users/me/',
            '/api/users/subscriptions/',
            '/api/tags/',
            f'/api/tags/{self.tag.pk}/',
            '/api/recipes/',
            f'/api/recipes/{self.recipe.pk}/',
            f'/api/ingredients/{self.ingredient.pk}/',
        )
        for page in pages:
            with self.subTest(page=page):
                response = self.auth_author.get(page)
                error_msg = (f'Ошибка: у {self.author.username}',
                             f'нет доступа к странице {page}')
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    error_msg
                )

    def test_shopping_cart_add(self):
        post = self.auth_follower.post(
            f'/api/recipes/{self.recipe_second.pk}/shopping_cart/')
        self.assertEqual(post.status_code, HTTPStatus.CREATED)
        self.assertEqual(len(post.data), 4)
        self.assertEqual(
            post.data, {'id': 2, 'name': 'Тестовый рецепт второй',
                        'image': '/media/default.jpg',
                        'cooking_time': 35})

    def test_get_shopping_card(self):
        response = self.auth_follower.get(
            '/api/recipes/download_shopping_cart/'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_shopping_cart_delete(self):
        delete = self.auth_follower.delete(
            f'/api/recipes/{self.recipe.pk}/shopping_cart/')
        self.assertIsNone(delete.data)
        self.assertEqual(delete.status_code, HTTPStatus.NO_CONTENT)

    def test_favorite(self):
        post = self.auth_follower.post(
            f'/api/recipes/{self.recipe.pk}/favorite/'
        )
        self.assertEqual(post.status_code, HTTPStatus.CREATED)
        self.assertEqual(len(post.data), 4)
        self.assertEqual(post.data, {'id': 1,
                                     'name':
                                     'Тестовый рецепт',
                                     'image': '/media/default.jpg',
                                     'cooking_time': 30})
        delete = self.auth_follower.delete(
            f'/api/recipes/{self.recipe.pk}/favorite/'
        )
        self.assertIsNone(delete.data)
        self.assertEqual(delete.status_code, HTTPStatus.NO_CONTENT)

    def test_subscribe(self):
        post = self.auth_follower.post(
            f'/api/users/{self.author.pk}/subscribe/')
        self.assertEqual(
            post.data,
            {'email': 'author@test.ru',
             'id': 2,
             'username': 'testauthor',
             'first_name': 'ИмяТест',
             'last_name': 'ФамилияТест',
             'is_subscribed': True,
             'recipes':
             [OrderedDict([('id', 1),
                           ('name', 'Тестовый рецепт'),
                           ('image', 'http://testserver/media/default.jpg'),
                           ('cooking_time', 30)]),
              OrderedDict([('id', 2),
                          ('name', 'Тестовый рецепт второй'),
                          ('image', 'http://testserver/media/default.jpg'),
                          ('cooking_time', 35)])], 'recipes_count': 2})
        self.assertEqual(len(post.data), 8)
        self.assertEqual(post.status_code, HTTPStatus.CREATED)
        delete = self.auth_follower.delete(
            f'/api/users/{self.author.pk}/subscribe/')
        self.assertIsNone(delete.data)
        self.assertEqual(delete.status_code, HTTPStatus.NO_CONTENT)

    def test_check_tags_in(self):
        response = self.auth_author.get('/api/recipes/')
        self.assertIn('tags', str(response.data))
        self.assertIn('#fffafa', str(response.data))

    def test_check_ingredients_in(self):
        response = self.auth_author.get('/api/recipes/')
        self.assertIn('ingredient', str(response.data))
        self.assertIn('Тестовый ингредиент', str(response.data))

    def test_create_recipe(self):
        post = self.auth_author.post(
            '/api/recipes/',
            {"ingredients": [{"id": 1, "amount": 10}], "tags": [1],
             "image": "data:image/png;base64,iVBO"
             + "Rw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABie"
             + "ywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXB"
             + "IWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAA"
             + "AAggCByxOyYQAAAABJRU5ErkJggg==",
             "name": "Новый рецепт",
             "text": "Тест описания",
             "cooking_time": 600}, format='json')
        self.assertEqual(post.status_code, HTTPStatus.CREATED)

    def test_patch_recipe(self):
        patch = self.auth_author.patch(
            f'/api/recipes/{self.recipe.pk}/',
            {"ingredients": [{"id": 1, "amount": 10}],
             "tags": [1], "image":
                "data:image/png;base64,iVBORw0KGgoAA"
                + "AANSUhEUgAAAAEAAAABAgMAAA"
                + "BieywaAAAACVBMVEUAAAD///9fX1/S0"
                + "ecCAAAACXBIWXMAAA7EAAAOxAGVKw4"
                + "bAAAACklEQVQImWNoAAAAgg"
                + "CByxOyYQAAAABJRU5ErkJggg==",
                "name": "Тест измененый рецепт",
                "text": "Тест описания",
                "cooking_time": 500}, format='json')
        self.assertEqual(patch.status_code, HTTPStatus.OK)
        self.assertIn('Тест измененый рецепт', str(patch.data))
        self.assertIn('500', str(patch.data))

    def test_delete_recipe(self):
        delete = self.auth_author.delete(f'/api/recipes/{self.recipe.pk}/')
        self.assertEqual(delete.status_code, HTTPStatus.NO_CONTENT)
        self.assertIsNone(delete.data)
