import base64
import djoser.serializers
from django.db.models import F
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers, mixins
from django.db.transaction import atomic


from recipes.models import Recipe, Tag, Ingredient, Subscriptions, Favorites, ShoppingCart, IngredientAmount

User = get_user_model()


class UserCreateSerializer(djoser.serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields=(
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
            )
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        user_id = obj.id if isinstance(obj, User) else obj.author.id
        request_user = self.context.get('request').user.id
        queryset = Subscriptions.objects.filter(author=user_id,
                                                user=request_user).exists()
        return queryset

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class UserSubSerializer(UserSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
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


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
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
        ingredients = obj.ingredient.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient_amount__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        return self.__is_user_anonymous(obj, Favorites)

    def get_is_in_shopping_cart(self, obj):
        return self.__is_user_anonymous(obj, ShoppingCart)

    def validate(self, data):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        keys = {'text', 'name', 'cooking_time'}
        errors={}
        for key in keys:
            if key not in data:
                errors.update({key: 'Обязательное поле'})
        if not tags or not ingredients:
            if tags:
                errors.update({'ingredients': 'Обязательное поле'})
            if ingredients:
                errors.update({'tags': 'Обязательное поле'})
        if errors:
            raise serializers.ValidationError(errors)
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
            recipe.tag.add(tag['id'])
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
            instance.tag.add(tag['id'])
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
