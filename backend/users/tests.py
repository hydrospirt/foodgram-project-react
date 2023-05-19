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

    def test_email_label(self):
        """verbose_name поля email совпадает с ожидаемым."""
        user = UserModelTest.user
        verbose = user._meta.get_field('email').verbose_name
        self.assertEqual(verbose, 'Адрес электронной почты')

    def test_email_help_text(self):
        """help_text поля title совпадает с ожидаемым."""
        user = UserModelTest.user
        help_text = user._meta.get_field('email').help_text
        self.assertEqual(help_text, 'Заполните адрес электронной почты')

    def test_username_label(self):
        """verbose_name поля username совпадает с ожидаемым."""
        user = UserModelTest.user
        verbose = user._meta.get_field('username').verbose_name
        self.assertEqual(verbose, 'Имя пользователя')

    def test_username_help_text(self):
        """help_text поля username совпадает с ожидаемым."""
        user = UserModelTest.user
        help_text = user._meta.get_field('username').help_text
        self.assertEqual(help_text, 'Заполните имя пользователя')

    def test_first_name_label(self):
        """verbose_name поля first_name совпадает с ожидаемым."""
        user = UserModelTest.user
        verbose = user._meta.get_field('first_name').verbose_name
        self.assertEqual(verbose, 'Имя')

    def test_first_name_help_text(self):
        """help_text поля username совпадает с ожидаемым."""
        user = UserModelTest.user
        help_text = user._meta.get_field('first_name').help_text
        self.assertEqual(help_text, 'Заполните свое настоящее имя')

    def test_last_name_label(self):
        """verbose_name поля last_name совпадает с ожидаемым."""
        user = UserModelTest.user
        verbose = user._meta.get_field('last_name').verbose_name
        self.assertEqual(verbose, 'Фамилия')

    def test_first_name_help_text(self):
        """help_text поля last_name совпадает с ожидаемым."""
        user = UserModelTest.user
        help_text = user._meta.get_field('last_name').help_text
        self.assertEqual(help_text, 'Заполните свою настоящую фамилию')

    def test_password_label(self):
        """verbose_name поля password совпадает с ожидаемым."""
        user = UserModelTest.user
        verbose = user._meta.get_field('password').verbose_name
        self.assertEqual(verbose, 'Пароль')

    def test_password_help_text(self):
        """help_text поля last_name совпадает с ожидаемым."""
        user = UserModelTest.user
        help_text = user._meta.get_field('password').help_text
        self.assertEqual(help_text, 'Введите пароль')
