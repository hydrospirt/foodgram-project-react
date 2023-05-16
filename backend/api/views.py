from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from djoser.views import UserViewSet
from rest_framework import viewsets, permissions, filters, status
from api.serializers import UserSerializer, TagSerializer, RecipeSerializer, IngredientSerializer, UserSubSerializer
from recipes.models import Recipe, Tag, Ingredient, Subscriptions

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
        print(pk)
        author = get_object_or_404(User, pk=pk)
        user = request.user
        if request.method == 'POST':
            if author == user:
                return Response(
                    {'errors': 'Вы не можете подписатся на себя'},
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
    search_fields = ('name', )
    filter_backends = (filters.SearchFilter,)
    http_method_names = ('get',)
