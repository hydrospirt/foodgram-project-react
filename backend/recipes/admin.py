from django.contrib import admin
from recipes.models import Recipe, Ingredient, Tag


class TagInline(admin.TabularInline):
    model = Tag


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    inlines = (TagInline,)
    list_filter = ('author', 'name', 'tag')
    search_fields = ('author', 'name', 'tag')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
