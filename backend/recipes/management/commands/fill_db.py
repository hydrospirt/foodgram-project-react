import csv
import json
import mimetypes
import os
from pathlib import Path
from typing import Any

from clint.textui import colored
from django.core.management.base import BaseCommand, CommandParser
from progress.bar import Bar
from recipes.models import Ingredient

PROJECT_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = os.path.join(PROJECT_DIR, 'data')


class Command(BaseCommand):
    help = 'Загружает данные из файлов CSV и JSON'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('file', type=str)

    def handle(self, *args: Any, **options: Any) -> str:
        file = os.path.join(DATA_DIR, options.get('file'))
        mimetype = self.check_file(file)
        self.clean_to_datebase()

        for i in Bar('Загрузка').iter(self.load_to_datebase(file, mimetype)):
            obj = Ingredient(**i)
            obj.save()
        self.stdout.write('Запись в базу данных успешно завершена...')

    def check_file(self, file):
        if not os.path.isfile(file):
            self.stderr.write(f'--- Файл {file} не найден')
            raise SystemExit
        self.stdout.write(
            colored.green('+++ Проверка пути файла успешно завершена...'))
        mimetype = mimetypes.MimeTypes().guess_type(file)[0]

        if mimetype not in ('text/csv', 'application/json'):
            self.stderr.write(
                f'--- Формат файла {file} не относится к CSV или JSON')
            raise SystemExit
        self.stdout.write(
            colored.green('+++ Проверка формата файла успешно завершена...'))

        return mimetype

    def clean_to_datebase(self):
        if Ingredient.objects.exists():
            answer = input(
                'Вы хотите очистить данные об ингредиентах? Д или Н: ')
            if answer.lower() == 'д':
                Ingredient.objects.all().delete()
            else:
                self.stderr.write('--- Запись невозможна. Очистите таблицу')
                raise SystemExit

    def load_to_datebase(self, file, mimetype):
        with open(file, newline='', encoding='utf-8') as f:
            try:
                if mimetype == 'text/csv':
                    data = csv.DictReader(
                        f, fieldnames=('name', 'measurement_unit'))
                else:
                    data = json.load(f)
            except (csv.Error, TypeError):
                self.stderr.write('--- Ошибка файла')
                raise SystemExit

            for i in data:
                yield i
