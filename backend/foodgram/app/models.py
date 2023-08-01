from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class Tag(models.Model):
    name = models.CharField(unique=True, max_length=20)
    color = models.CharField(unique=True, max_length=7,
        validators=[
            RegexValidator(
                regex='^#([a-fA-F0-9]{6})$',
                message='Not HEX!'
            )
        ]
    )
    slug = models.SlugField(unique=True, max_length=20)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}, {self.unit}'
    

class Recipe(models.Model):

    # class TagsList(models.TextChoices):
    #     FRESHMAN = 'FR', _('Freshman')
    #     SOPHOMORE = 'SO', _('Sophomore')
    #     JUNIOR = 'JR', _('Junior')
    #     SENIOR = 'SR', _('Senior')
    #     GRADUATE = 'GR', _('Graduate')

    # Автор публикации (пользователь).
    #author = models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    # Название.
    name = models.CharField(max_length=50)
    # Картинка.
    image = models.ImageField(upload_to='recipe/images/', null=True, default=None)
    # Текстовое описание.
    text = models.TextField()
    # Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
    ingredients = models.ManyToManyField(Ingredient, through='IngredientsRecipe', related_name='recipes')
    # Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
    tags = models.ManyToManyField(Tag, related_name='recipes')

    # Время приготовления в минутах.
    cooking_time = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}'