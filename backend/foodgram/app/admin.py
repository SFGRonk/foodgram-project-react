from django.contrib import admin
from .models import *

# class RecipeAdmin(admin.ModelAdmin):
#     # list_display = (
#     #     'name',
#     #     'image',
#     #     'text',
#     #     'cooking_time',
#     #     #'author',
#     # )
#     #list_editable = ('author',)
#     search_fields = ('text',)
#     #list_filter = ('name',)
#     #empty_value_display = '-пусто-'


admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientsRecipe)