# public/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('', home_dashboard, name='home_dashboard'),
    path('categorias/', category_list, name='category_list'),
    path('categorias/create/', category_create, name='category_create'),
    path('categorias/delete/<int:pk>/', category_delete, name='category_delete'),
]
