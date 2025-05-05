from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django_tenants.utils import get_tenant_model, tenant_context
from getpass import getpass

class Command(BaseCommand):
    help = 'Cria um superusuário para um tenant específico'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, required=True, help='Schema do tenant')

    def handle(self, *args, **options):
        schema_name = options['schema']
        TenantModel = get_tenant_model()

        try:
            tenant = TenantModel.objects.get(schema_name=schema_name)
        except TenantModel.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"❌ Tenant '{schema_name}' não encontrado."))
            return

        username = input("Digite o nome de usuário: ").strip()
        email = input("Digite o email: ").strip()
        password = getpass("Digite a senha: ")
        password2 = getpass("Confirme a senha: ")

        if password != password2:
            self.stderr.write(self.style.ERROR("❌ As senhas não coincidem."))
            return

        with tenant_context(tenant):
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"⚠️ Usuário '{username}' já existe no schema '{schema_name}'."))
            else:
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f"✅ Superusuário '{username}' criado com sucesso no schema '{schema_name}'"))
