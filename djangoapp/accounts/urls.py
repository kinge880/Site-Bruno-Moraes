from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]