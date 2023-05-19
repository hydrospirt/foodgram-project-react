from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
        help_text='Заполните адрес электронной почты',
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+\Z')]),
        help_text='Заполните имя пользователя'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        help_text='Заполните свое настоящее имя'
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        help_text='Заполните свою настоящую фамилию'
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150,
        help_text='Введите пароль'
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        verbose_name='Персонал',
        default=False,
    )
    last_login = models.DateTimeField(
        verbose_name='Время последнего посещения',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
