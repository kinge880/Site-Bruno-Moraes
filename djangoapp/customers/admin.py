from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Cliente, Domain
from django_tenants.utils import get_tenant

# Formulário para Cliente
class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

    def clean_schema_name(self):
        schema = self.cleaned_data['schema_name']
        if schema == 'public':
            raise ValidationError("O schema 'public' é reservado e não pode ser usado.")
        return schema

# Admin do Cliente
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm
    list_display = ('nome', 'schema_name', 'email_contato', 'criado_em')
    search_fields = ('nome', 'schema_name', 'email_contato')
    list_filter = ('criado_em',)
    ordering = ('-criado_em',)

    def has_module_permission(self, request):
        tenant = get_tenant(request)
        return request.user.is_superuser


# Formulário para Domain
class DomainForm(ModelForm):
    class Meta:
        model = Domain
        fields = '__all__'

    def clean_domain(self):
        domain = self.cleaned_data['domain'].strip().lower()
        if Domain.objects.filter(domain=domain).exists():
            raise ValidationError("Este domínio já está em uso.")
        return domain

# Admin do Domain
class DomainAdmin(admin.ModelAdmin):
    form = DomainForm
    list_display = ('domain', 'tenant', 'is_primary')
    search_fields = ('domain',)
    list_filter = ('is_primary',)

    def has_module_permission(self, request):
        tenant = get_tenant(request)
        return request.user.is_superuser


# Registro dos models
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Domain, DomainAdmin)
