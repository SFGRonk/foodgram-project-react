from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('app/', views.index),
    # path('group_list.html', views.group_list, name='group_list'),
    # path('group/<int:pk>/', views.group_posts_pk, name='group_int'),   
] 