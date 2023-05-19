from django.test import TestCase

from users.models import CustomUser


class UserModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create(
            email='test@test.ru',
            username='testuser',
            first_name='First_test',
            last_name='Last_test',
            password='Gsdfks5252',
        )

    def test_verbose_name(self):
        """verbose_name всех полей совпадает с ожидаемым."""
        user = UserModelTest.user
        field_verboses = {
            'email': 'Адрес электронной почты',
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'password': 'Пароль'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    user._meta.get_field(value).verbose_name, expected
                )

    def test_help_text(self):
        user = UserModelTest.user
        field_help_texts = {
            'email': 'Заполните адрес электронной почты',
            'username': 'Заполните имя пользователя',
            'first_name': 'Заполните свое настоящее имя',
            'last_name': 'Заполните свою настоящую фамилию',
            'password': 'Введите пароль',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    user._meta.get_field(value).help_text, expected
                )
