from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status
from api.serializers import UserSerializer, TagSerializer, RecipeSerializer, IngredientSerializer
from recipes.models import Recipe, Tag, Ingredient

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
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
