from django.shortcuts import render
from rest_framework import viewsets, permissions
from api.serializers import UserSerializer, TagSerializer, RecipeSerializer, IngredientSerializer
from recipes.models import Recipe, Tag, Ingredient
from users.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('get',)



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('get',)
