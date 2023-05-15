from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import CustomUserViewSet, TagViewSet, RecipeViewSet, IngredientViewSet

router = DefaultRouter()
router.register(r'tag', TagViewSet, basename='tag')
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
