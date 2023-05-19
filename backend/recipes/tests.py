from django.test import TestCase
from recipes.models import Recipe, Tag, Ingredient, IngredientAmount, Subscriptions, Favorites, ShoppingCart


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

    def test_name_label(self):
        """verbose_name поля name совпадает с ожидаемым."""
        ingredient = IngredientModelTest.ingredient
        verbose = ingredient._meta.get_field('name').verbose_name
        self.assertEqual(verbose, 'Название')

    def test_measurement_unit_label(self):
        """verbose_name поля measurement_unit совпадает с ожидаемым."""
        ingredient = IngredientModelTest.ingredient
        verbose = ingredient._meta.get_field('measurement_unit').verbose_name
        self.assertEqual(verbose, 'Единица измерения')
