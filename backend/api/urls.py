from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import CustomUserViewSet, TagViewSet

router = DefaultRouter()
router.register(r'tag', TagViewSet, basename='tag')
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
