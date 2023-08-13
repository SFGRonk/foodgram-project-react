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

router.register('api/recipes', RecipeViewSet)
router.register('api/ingredients', IngredientViewSet)
router.register('api/tags', TagViewSet)
router.register('api/users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
