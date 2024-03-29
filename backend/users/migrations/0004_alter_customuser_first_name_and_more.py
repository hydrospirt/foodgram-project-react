# Generated by Django 4.2.1 on 2023-05-22 12:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(help_text='Заполните свое настоящее имя', max_length=150, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(help_text='Заполните свою настоящую фамилию', max_length=150, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(help_text='Введите пароль', max_length=150, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(help_text='Заполните имя пользователя', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(regex='^[\\w.@+-]+\\Z')], verbose_name='Имя пользователя'),
        ),
    ]
