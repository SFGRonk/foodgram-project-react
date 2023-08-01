from django.shortcuts import render
from django.http import HttpResponse
from .models import Recipe


def index(request):
    recipe = Recipe.objects.all()
    #recipe = recipe.get
    return HttpResponse(recipe)
