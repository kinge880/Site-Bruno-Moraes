from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from .models import FaleComigo

@admin.register(FaleComigo)
class FaleComigoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'status_visualizado', 'dtmov', 'acoes')
    list_filter = ('visualizado', 'dtmov')
    search_fields = ('nome', 'email', 'telefone', 'descricao')
    ordering = ('-dtmov',)

    def status_visualizado(self, obj):
        """Exibe um indicador visual para mensagens lidas/não lidas"""
        if obj.visualizado:
            return format_html('<span style="color: green; font-weight: bold;">✔ Lido</span>')
        return format_html('<span style="color: red; font-weight: bold;">✖ Não Lido</span>')
    status_visualizado.short_description = "Status"

    def acoes(self, obj):
        """Gera um link para abrir a mensagem no Django Admin"""
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html('<a href="{}" style="color: blue; font-weight: bold;">📩 Abrir</a>', url)
    acoes.short_description = "Ações"

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Marca como visualizado ao abrir a mensagem"""
        obj = self.get_object(request, object_id)
        if obj and not obj.visualizado:
            obj.visualizado = True
            obj.save(update_fields=['visualizado'])
        return super().change_view(request, object_id, form_url, extra_context)
