from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Cliente(TenantMixin):
    nome = models.CharField(max_length=100)
    email_contato = models.EmailField()
    telefone = models.CharField(max_length=20, blank=True, null=True)

    # Dados de faturamento
    cnpj = models.CharField(max_length=18, blank=True, null=True)
    razao_social = models.CharField(max_length=100, blank=True, null=True)
    endereco_faturamento = models.TextField(blank=True, null=True)

    # Controle de acesso
    em_trial = models.BooleanField(default=True)
    trial_expira_em = models.DateField(blank=True, null=True)
    contas_em_dia = models.BooleanField(default=True)
    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    auto_create_schema = True

    def __str__(self):
        return self.nome

class Domain(DomainMixin):
    pass  # pode customizar depois se quiser campos extras

class Pagamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagamentos')
    data_referencia = models.DateField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)
    observacao = models.TextField(blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.data_referencia} - {'Pago' if self.pago else 'Pendente'}"