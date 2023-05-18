from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from rest_framework.decorators import action, permission_classes, renderer_classes
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework import viewsets, permissions, filters, status
from api.serializers import UserSerializer, TagSerializer, RecipeSerializer, IngredientSerializer, UserSubSerializer, ShortRecipeSerializer, IngredientAmountSerializer
from recipes.models import Recipe, Tag, Ingredient, Subscriptions, Favorites, ShoppingCart
from api.permissions import IsAuthorOrAdminOrReadOnly, IsAdminOrReadOnly
from django.http import FileResponse
from api.renders import IngredientDataRendererTXT
from django.db.models import F, Sum

User = get_user_model()


class UserViewSet(UserViewSet, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
            methods=('GET',),
            detail=False,
            url_path='me',
            url_name='me',)
    @permission_classes([permissions.IsAuthenticated])
    def me(self, request, *args, **kwargs):
        try:
            self.object = User.objects.get(pk=request.user.id)
            serializer = self.get_serializer(self.object)
            return Response(serializer.data)
        except:
            return Response(
                {"detail": "Ошибка авторизации."},
                status=status.HTTP_401_UNAUTHORIZED
                )

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
        elif request.method == 'DELETE':
            try:
                Subscriptions.objects.get(author=author, user=user).delete()
            except Subscriptions.DoesNotExist:
                return Response(
                    {'errors': f'Вы не подписаны на пользователя c ID: {pk}'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=('GET',),
            detail=False,)
    @permission_classes([permissions.IsAuthenticated])
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        subs = User.objects.filter(subscribing__user=user)
        serializer = UserSubSerializer(subs, context={'request': request}, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

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
        elif request.method == 'DELETE':
            try:
                Favorites.objects.get(user=user, recipe=recipe).delete()
            except Favorites.DoesNotExist:
                return Response(
                    {'errors': f'Рецепта нет в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
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
        elif request.method == 'DELETE':
            try:
                ShoppingCart.objects.get(user=user, recipe=recipe).delete()
            except ShoppingCart.DoesNotExist:
                return Response(
                    {'errors': f'Рецепта нет в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=('GET',),
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        renderer_classes=[IngredientDataRendererTXT])
    def download_shopping_cart(self, request, *args, **kwargs):
        user = request.user
        queryset = Ingredient.objects.filter(
            ingredient_amount__recipe__shopping_cart__user=user
            ).values(
            'name',
            'measurement_unit',
            ).annotate(amount=Sum('ingredient_amount__amount'))
        serializer = IngredientAmountSerializer(queryset, many=True)
        file_name = 'foodgram_shopping_cart.txt'
        return Response(serializer.data, headers={"Content-Disposition": f'attachment; filename="{file_name}"'})



class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name', )
    filter_backends = (filters.SearchFilter,)
