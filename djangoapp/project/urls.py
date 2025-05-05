from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Flow Hub"
admin.site.site_title = "Flow Hub Admin"
admin.site.index_title = "Painel de Controle"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('public.urls')),
    path('', include('accounts.urls')),
    path('meu-painel/', include('bi.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, 
        document_root=settings.STATIC_ROOT
    )
