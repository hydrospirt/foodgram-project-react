from urllib.parse import unquote

from api.filters import RecipeFilter
from api.paginators import LimitPageNumberPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from api.renders import IngredientDataRendererTXT
from api.serializers import (IngredientAmountSerializer, IngredientSerializer,
                             RecipeSerializer, ShortRecipeSerializer,
                             TagSerializer, UserCreateSerializer,
                             UserSerializer, UserSubSerializer)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorites, Ingredient, Recipe, ShoppingCart,
                            Subscriptions, Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

User = get_user_model()


class ErrorMessage:
    SUB_MSG_ERROR = {'errors': 'Вы не подписаны на данного пользователя'}
    FAV_MSG_ERROR = {'error': 'Рецепт уже добавлен в избранное'}
    FAV_NO_RECIPE_ERROR = {'errors': 'Рецепта нет в избранном'}
    RECIPE_ALREADY_IN_ERROR = {'errors': 'Рецепта нет в избранном'}
    SHOP_NO_RECIPE_ERROR = {'errors': 'Рецепта нет в списке покупок'}


class UserViewSet(UserViewSet, viewsets.ModelViewSet, ErrorMessage):
    queryset = User.objects.all()
    permission_classes = (DjangoModelPermissions,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer

    @action(methods=('GET',),
            detail=False,
            url_path='me',
            url_name='me',
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        self.object = User.objects.get(pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(methods=('POST', 'DELETE'),
            detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, *args, **kwargs):
        pk = kwargs.get('id',)
        author = get_object_or_404(User, pk=pk)
        user = self.request.user
        if request.method == 'POST':
            serializer = UserSubSerializer(
                author, data=request.data, context={'request': request}
            )
            if serializer.is_valid():
                sub = Subscriptions(author=author, user=user)
                sub.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            sub = Subscriptions.objects.filter(author=author, user=user)
            if sub.exists():
                sub.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                self.SUB_MSG_ERROR,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=('GET',),
            detail=False,
            permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        subs = User.objects.filter(subscribing__user=user)
        pages = self.paginate_queryset(subs)
        serializer = UserSubSerializer(
            pages, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet, ErrorMessage):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = LimitPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    @action(methods=('POST', 'DELETE'),
            detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        fav_filter = Favorites.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if fav_filter.exists():
                return Response(
                    self.FAV_MSG_ERROR,
                    status=status.HTTP_400_BAD_REQUEST
                )
            fav = Favorites(user=user, recipe=recipe)
            fav.save()
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if fav_filter.exists():
                fav_filter.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                self.FAV_NO_RECIPE_ERROR,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=('POST', 'DELETE'),
            detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        shopcart_fliter = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if request.method == 'POST':
            if shopcart_fliter.exists():
                return Response(
                    self.RECIPE_ALREADY_IN_ERROR,
                    status=status.HTTP_400_BAD_REQUEST
                )
            shopcart = ShoppingCart(user=user, recipe=recipe)
            shopcart.save()
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if shopcart_fliter.exists():
                shopcart_fliter.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                self.SHOP_NO_RECIPE_ERROR,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        renderer_classes=[IngredientDataRendererTXT])
    def download_shopping_cart(self, request, *args, **kwargs):
        user = request.user
        queryset = Ingredient.objects.filter(
            ingredient_amount__recipe__shopping_cart__user=user).values(
            'name',
            'measurement_unit'
        ).annotate(amount=Sum('ingredient_amount__amount'))
        serializer = IngredientAmountSerializer(queryset, many=True)
        return Response(
            serializer.data,
            headers={"Content-Disposition":
                     f'attachment; filename="{settings.FILE_NAME}"'})


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.GET.get('name', '')
        if name:
            if name[0] == '%':
                name = unquote(name)
            name = name.lower()
            icontains_query = queryset.filter(name__icontains=name)
            queryset = icontains_query
            return queryset
        return queryset
