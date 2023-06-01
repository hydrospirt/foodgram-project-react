from django_filters import ChoiceFilter, FilterSet, ModelMultipleChoiceFilter
from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    STATUS_CHOICES = (
        (0, 'false'),
        (1, 'true'),)
    is_favorited = ChoiceFilter(method='filter_is_favorited',
                                choices=STATUS_CHOICES)
    is_in_shopping_cart = ChoiceFilter(
        method='filter_is_in_shopping_cart',
        choices=STATUS_CHOICES)

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
        )

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user

        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(shopping_cart__user=user)
        return queryset
