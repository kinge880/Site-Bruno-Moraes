from django.http import HttpResponse
from django_tenants.utils import get_tenant

class ChecaPagamentoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = get_tenant(request)
        if hasattr(tenant, "ativo") and not tenant.ativo:
            return HttpResponse("Este ambiente está temporariamente suspenso por pendência de pagamento.", status=403)
        return self.get_response(request)
