from django.shortcuts import render
from rest_framework import viewsets

from api.serializers import CustomUserSerializer, TagSerializer
from recipes.models import Recipe, Tag, Ingredient
from users.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer