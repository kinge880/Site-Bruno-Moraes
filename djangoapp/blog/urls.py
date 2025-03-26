from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='base_blog'),
    path('post/', views.create_blog_post, name='create_blog_post'),
    path('<str:categoria>/', views.index, name='category_filter'),
    path('<int:year>/<int:month>/', views.index, name='archive_filter'),
    path('<str:categoria>/<slug:slug>/', views.blog_post_detail, name='blog_detail'),
    path('<str:categoria>/<slug:slug>/get-comments/', views.get_comments, name='get_comments'),
    path('<str:categoria>/<slug:slug>/comment/', views.post_comment, name='post_comment'),
    path('<str:categoria>/<slug:slug>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('<str:categoria>/<slug:slug>/comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )