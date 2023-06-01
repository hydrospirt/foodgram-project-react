from django.contrib.auth import get_user_model
from django_filters import FilterSet, ModelMultipleChoiceFilter, BooleanFilter
from recipes.models import Recipe, Tag, ShoppingCart, Favorites

User = get_user_model()

class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
        )

    def filter_is_favorited(self, queryset, value):
        user = self.request.user
        if int(value) and not user.is_anonymous:
            return queryset.filter(favorites__user__exact=user)
        return queryset.exclude(favorites__user__exact=user)


    def filter_is_in_shopping_cart(self, queryset, value):
        user = self.request.user
        if int(value) and not user.is_anonymous:
            return queryset.filter(shopping_cart__user__exact=user)
        return queryset.exclude(shopping_cart__user__exact=user)