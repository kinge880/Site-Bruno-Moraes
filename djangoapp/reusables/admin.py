from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from .models import FaleComigo

@admin.register(FaleComigo)
class FaleComigoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'status_visualizado', 'dtmov', 'acoes')
    list_filter = ('visualizado', 'dtmov')
    search_fields = ('nome', 'email', 'telefone', 'descricao', 'endereco', 'informacoes_adicionais')
    ordering = ('-dtmov',)
    readonly_fields = ('dtmov', 'visualizado', 'preview_imagem')

    fieldsets = (
        (None, {
            'fields': ('nome', 'telefone', 'email', 'endereco')
        }),
        ('Reivindicação', {
            'fields': ('descricao', 'imagem', 'preview_imagem', 'informacoes_adicionais')
        }),
        ('Sistema', {
            'fields': ('visualizado', 'dtmov')
        }),
    )

    def status_visualizado(self, obj):
        if obj.visualizado:
            return format_html('<span style="color: green; font-weight: bold;">✔ Lido</span>')
        return format_html('<span style="color: red; font-weight: bold;">✖ Não Lido</span>')
    status_visualizado.short_description = "Status"

    def acoes(self, obj):
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html('<a href="{}" style="color: blue; font-weight: bold;">📩 Abrir</a>', url)
    acoes.short_description = "Ações"

    def preview_imagem(self, obj):
        if obj.imagem and hasattr(obj.imagem, 'url'):
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-height: 200px; max-width: 100%; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);" />'
                '</a>',
                obj.imagem.url,
                obj.imagem.url
            )
        return format_html('<span style="color: #999;">Sem imagem enviada</span>')
    preview_imagem.short_description = "Prévia da Imagem"


    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and not obj.visualizado:
            obj.visualizado = True
            obj.save(update_fields=['visualizado'])
        return super().change_view(request, object_id, form_url, extra_context)
    
    