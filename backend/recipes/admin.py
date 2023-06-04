from django.contrib import admin
from recipes.models import (Favorites, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Subscriptions, Tag)

admin.site.site_header = 'Проект Foodgram'
admin.site.index_title = 'Панель Администратора'
admin.site.site_title = 'Проект Foodgram'


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'short_text',
        'amount_favorites',
        'pub_date',
    )
    list_filter = ('tags',)
    search_fields = ('author', 'author__email', 'name')
    readonly_fields = ('amount_favorites',)
    inlines = (IngredientAmountInline,)
    date_hierarchy = 'pub_date'
    empty_value_display = '-пусто-'

    @admin.display(description='Кол-во добавлений в избранное')
    def amount_favorites(self, obj):
        return obj.favorites.count()

    @admin.display(description='Текст')
    def short_text(self, obj):
        return obj.text[:20]


@admin.register(Ingredient)
class AdminIngredient(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    list_filter = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Favorites)
class AdminFavorites(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_filter = ('recipe__tags',)
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name',
    )
    empty_value_display = '-пусто-'


@admin.register(Subscriptions)
class AdminSubscriptions(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'author',
    )
    search_fields = (
        'user__username',
        'user__email',
        'author__username',
        'author__email',
    )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class AdminShoppingCart(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_filter = ('recipe__tags',)
    search_fields = (
        'user__username',
        'user__email',
        'recipe__name',
    )
    empty_value_display = '-пусто-'
