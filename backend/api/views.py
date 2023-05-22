from itertools import chain

from api.paginators import LimitPageNumberPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly
from api.renders import IngredientDataRendererTXT
from api.serializers import (IngredientAmountSerializer, IngredientSerializer,
                             RecipeSerializer, ShortRecipeSerializer,
                             TagSerializer, UserSerializer, UserSubSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import (Favorites, Ingredient, Recipe, ShoppingCart,
                            Subscriptions, Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

User = get_user_model()


class UserViewSet(UserViewSet, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=('GET',),
            detail=False,
            url_path='me',
            url_name='me',)
    @permission_classes([permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        self.object = User.objects.get(pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action(methods=('POST', 'DELETE'),
            detail=True,)
    @permission_classes([permissions.IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        pk = kwargs.get('id',)
        author = get_object_or_404(User, pk=pk)
        user = request.user
        if request.method == 'POST':
            if author == user:
                return Response(
                    {'errors': 'Вы не можете подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST)
            if Subscriptions.objects.filter(author=author, user=user).exists():
                return Response(
                    {'errors': 'Вы подписаны на этого пользователя'},
                    status=status.HTTP_400_BAD_REQUEST)
            sub = Subscriptions(author=author, user=user)
            sub.save()
            serializer = UserSubSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                Subscriptions.objects.get(author=author, user=user).delete()
            except Subscriptions.DoesNotExist:
                return Response(
                    {'errors': f'Вы не подписаны на пользователя c ID: {pk}'},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=('GET',),
            detail=False,)
    @permission_classes([permissions.IsAuthenticated])
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        subs = User.objects.filter(subscribing__user=user)
        serializer = UserSubSerializer(
            subs, context={'request': request}, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author')
        if author:
            return queryset.filter(author=author)
        tags = self.request.query_params.getlist('tags')
        if tags:
            return queryset.filter(tags__slug__in=tags).distinct()
        if self.request.user.is_anonymous:
            return queryset
        return queryset

    @action(methods=('POST', 'DELETE'),
            detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            if Favorites.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            fav = Favorites(user=user, recipe=recipe)
            fav.save()
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                Favorites.objects.get(user=user, recipe=recipe).delete()
            except Favorites.DoesNotExist:
                return Response(
                    {'errors': 'Рецепта нет в избранном'},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=('POST', 'DELETE'),
            detail=True,
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'error': 'Рецепт уже добавлен в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            fav = ShoppingCart(user=user, recipe=recipe)
            fav.save()
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                ShoppingCart.objects.get(user=user, recipe=recipe).delete()
            except ShoppingCart.DoesNotExist:
                return Response(
                    {'errors': 'Рецепта нет в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_204_NO_CONTENT)
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
        file_name = 'foodgram_shopping_cart.txt'
        return Response(
            serializer.data,
            headers={"Content-Disposition":
                     f'attachment; filename="{file_name}"'})


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.GET.get('search', '')
        if name:
            name = name.lower()
            istartwith_query = queryset.filter(name__istartswith=name)
            icontains_query = queryset.filter(name__icontains=name)
            results = set(chain(istartwith_query, icontains_query))
            queryset = results
            return queryset
        return super().get_queryset()
