from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.basehome, name='paginicial'),
    path('login/', views.login, name='login'),
    path('deslogar/', views.logout_view, name='logou'),
    path('cadastro/banner/inicio/', views.cadastrar_banner_inicio, name='cadastrar_banner_inicio'),
    path('atualizar-banner/<int:banner_id>/', views.atualizar_banner_inicio, name='atualizar_banner_inicio'),
    path('deletar-banner/<int:banner_id>/', views.deletar_banner_inicio, name='deletar_banner_inicio'),
    path('listar-banners/', views.listar_banners, name='listar_banners'),
    
    path('post-minha-historia/', views.post_minha_historia, name='post_minha_historia'),
    
    path('post-banner-campanha/', views.post_banner_campanha, name='post_banner_campanha'),
    
    path('propostas/', views.listar_propostas, name='listar_propostas'),
    path('propostas/cadastrar/', views.cadastrar_proposta, name='cadastrar_proposta'),
    path('propostas/deletar/<int:id>/', views.deletar_proposta, name='deletar_proposta'),
    
    path('fale/', views.fale_comigo, name='fale_comigo'),
    
    path('sobre/', views.sobre_mim, name='sobre_mim'),
    path("webhook/", views.webhook),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )