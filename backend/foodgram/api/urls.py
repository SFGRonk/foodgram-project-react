from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    CustomUserViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
