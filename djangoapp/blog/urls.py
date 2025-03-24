from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='base_blog'),
    path('postar/', views.create_blog_post, name='create_blog_post'),
    path('<str:categoria>/', views.index, name='category_filter'),
    path('<int:year>/<int:month>/', views.index, name='archive_filter'),
    path('<str:categoria>/<slug:slug>/', views.post_detail, name='blog_detail'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )