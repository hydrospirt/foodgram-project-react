from datetime import datetime
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from http import HTTPStatus
from recipes.models import Tag, Recipe

User = get_user_model()

class ApiURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest = Client()
        cls.user = User.objects.create_user(username='testman',
                                            email='tester@test.ru')
        cls.author = User.objects.create_user(username='testauthor',
                                              email='author@test.ru')
        cls.tag = Tag.objects.create(
            name='Тест',
            color='#fffafa',
            slug='test',
        )
        cls.recipe = Recipe.objects.create(
            author=cls.author,
            name='Тестовый рецепт',
            text='Тестовое описание',
            cooking_time=30,
            pub_date=datetime.now()
        )

    def test_api_guest_urls(self):
        pages = (
            '/api/users/',
            '/api/tags/',
            f'/api/tags/{self.tag.pk}/',
            '/api/recipes/',
            f'/api/recipes/{self.recipe.pk}/'

        )
        for page in pages:
            with self.subTest(page=page):
                response = self.guest.get(page)
                error_msg = (f'Ошибка: у {self.user.username}',
                             f'нет доступа к странице {page}')
                self.assertEqual(
                    response.status_code,
                    HTTPStatus.OK,
                    error_msg
                )