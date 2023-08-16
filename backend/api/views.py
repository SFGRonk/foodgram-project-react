from app.models import (
    Recipe, Tag, Ingredient, IngredientInRecipe, Favorite, ShoppingCart
)
from users.models import User, Subscribe
from .serializers import (
    RecipeReadSerializer,
    RecipeWriteSerializer,
    RecipeLessSerializer,
    TagSerializer,
    IngredientSerializer,
    SubscribeSerializer
)
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly

from djoser.views import UserViewSet
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags',)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.add_del(Favorite, request, pk)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.add_del(ShoppingCart, request, pk)

    def add_del(self, model, request, pk):
        obj = model.objects.filter(user=request.user, recipe__id=pk)
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if not obj.exists():
                model.objects.create(user=request.user, recipe=recipe)
                serializer = RecipeLessSerializer(recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {f'ERR: {recipe.name} - already added'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {f'ERR: {recipe.name} - already deleted'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        if not request.user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = IngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))

        shopping_cart = ''
        for i in ingredients:
            shopping_cart += (
                f'{i["ingredient__name"]} '
                '\n'
                f'{i["amount"]} '
                f'{i["ingredient__measurement_unit"]} \n\n'
            )
        response = HttpResponse(shopping_cart, content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment;'
            'filename="shopping_cart.pdf"'
        )
        p = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
        p.setFont('Arial', 10)
        p.drawString(10, 800, shopping_cart)
        p.showPage()
        p.save()
        return response


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeSerializer(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscribe.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscribe,
                user=user,
                author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False)
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribing__user=user)
        serializer = SubscribeSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
