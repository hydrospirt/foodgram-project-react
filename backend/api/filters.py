from django_filters import FilterSet
from recipes.models import Recipe


class RecipeFilter(FilterSet):

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags__slug',
        )
