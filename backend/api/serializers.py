import base64

import djoser.serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.models import F
from django.db.transaction import atomic
from recipes.models import (Favorites, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Subscriptions, Tag)
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

User = get_user_model()


class ErrorMessage:
    ALREADY_FOLLOWED_ERROR = {'errors': 'Вы уже подписаны '
                              + 'на этого пользователя'}
    AUTHOR_FOLLOWED_ERROR = {'errors': 'Вы не сможете подписаться на себя'}
    TIME_COOKING_ERROR = {'detail': 'Время приготовления дожно быть больше, '
                          + f'либо равно {settings.MIN_TIME_COOKING} минуте'}
    MIN_AMOUNT_ERROR = {'amount': 'Укажите количество, '
                        f'которое больше, либо равно {settings.MIN_AMOUNT}'}
    ALREADY_INGREDIENT_ERROR = {'errors': 'Нельзя добавлять '
                                + 'одинаковые ингредиенты'}
    ID_MSG_ERROR = {'id': 'id элемента, не может быть отрицательным'}


class UserCreateSerializer(djoser.serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        user_id = obj.id
        request_user = self.context.get('request').user.id
        return Subscriptions.objects.filter(author=user_id,
                                            user=request_user).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class UserSubSerializer(UserSerializer, ErrorMessage):
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscriptions.objects.filter(author=author, user=user).exists():
            raise ValidationError(
                self.ALREADY_FOLLOWED_ERROR,
                status=status.HTTP_400_BAD_REQUEST
            )
        if user == author:
            raise ValidationError(
                self.AUTHOR_FOLLOWED_ERROR,
                status=status.HTTP_400_BAD_REQUEST
            )
        return data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer, ErrorMessage):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def __is_user_anonymous(self, obj, model):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return model.objects.filter(recipe=obj, user=user).exists()

    def get_ingredients(self, obj):
        return obj.ingredient.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('ingredient_amount__amount'))

    def get_is_favorited(self, obj):
        return self.__is_user_anonymous(obj, Favorites)

    def get_is_in_shopping_cart(self, obj):
        return self.__is_user_anonymous(obj, ShoppingCart)

    def validate_cooking_time(self, data):
        if data < settings.MIN_TIME_COOKING:
            raise serializers.ValidationError(
                self.TIME_COOKING_ERROR)
        return data

    def validate(self, data):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        keys = {'text', 'name', 'cooking_time'}
        errors = {}
        for key in keys:
            if key not in data:
                errors.update({key: 'Обязательное поле'})
        if not tags:
            errors.update({'tags': 'Обязательное поле'})
        if not ingredients:
            errors.update({'ingredients': 'Обязательное поле'})
        if errors:
            raise serializers.ValidationError(errors)

        for ingredient in ingredients:
            if int(ingredient['amount']) < settings.MIN_AMOUNT:
                raise serializers.ValidationError(self.MIN_AMOUNT_ERROR)
            if int(ingredient['id']) < 0:
                raise serializers.ValidationError(
                    self.ID_MSG_ERROR)
        ingredients_ids = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients) != len(set(ingredients_ids)):
            raise serializers.ValidationError(
                self.ALREADY_INGREDIENT_ERROR)
        data.update({
            'tags': tags,
            'ingredients': ingredients,
        }
        )
        return data

    @atomic
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        objects = []
        for ingredient in ingredients:
            ingredient = objects.append(IngredientAmount(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                amount=ingredient['amount'],
            ))
        IngredientAmount.objects.bulk_create(objects)
        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        for field, value in validated_data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
        objects = []
        instance.ingredient.clear()
        for ingredient in ingredients:
            ingredient = objects.append(IngredientAmount(
                recipe=instance,
                ingredient=Ingredient.objects.get(pk=ingredient['id']),
                amount=ingredient['amount'],
            ))
        IngredientAmount.objects.bulk_create(objects)
        for tag in tags:
            instance.tags.add(tag)
        instance.save()
        return instance


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    amount = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = (
            'name',
            'amount',
            'measurement_unit'
        )
