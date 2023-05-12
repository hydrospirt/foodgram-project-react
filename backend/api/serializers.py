from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            )