from unicodedata import name
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from reusables import views as viewsreusables

urlpatterns = [
    path('', views.land_home, name='land_home'),
    path('salvar-formulario-curso/', views.salvar_formulario_curso, name='salvar_formulario_curso'),
    path('formulario-sucesso/', views.formulario_sucesso, name='formulario_sucesso'),
    path('login/', viewsreusables.login, name='login'),
    path('deslogar/', viewsreusables.logout_view, name='logou'),
    path('redes/', viewsreusables.ancoraLinks, name='ancora_links'),
    path('redes/cadastrar/', viewsreusables.cadastrarLink, name='cadastrar_link'),
    path('redes/deletar/<int:link_id>/', viewsreusables.deletarLink, name='deletar_link'),
    path('politica-de-privacidade/', views.politica_privacidade, name='politica_privacidade'),
    path('sobre-nos/', views.sobre_nos, name='sobre_nos'),
    path('termos-de-uso/', views.termos_de_uso, name='termos_de_uso'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )