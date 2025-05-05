from django.core.management.base import BaseCommand
from customers.models import Cliente

class Command(BaseCommand):
    help = 'Deleta um tenant FlowBi (incluindo schema e domínios)'

    def handle(self, *args, **options):
        print("⚠️  Atenção: esta ação é irreversível.")
        schema_name = input("➡️ Nome do schema a ser deletado: ").strip()

        if schema_name == "public":
            self.stderr.write(self.style.ERROR("❌ O schema 'public' não pode ser deletado."))
            return

        try:
            tenant = Cliente.objects.get(schema_name=schema_name)

            confirm = input(f"⚠️ Tem certeza que deseja deletar o tenant '{tenant.nome}' (schema: {schema_name})? [s/N]: ").lower()
            if confirm != 's':
                self.stdout.write("❎ Ação cancelada.")
                return

            tenant.delete(force_drop=True)  # força exclusão do schema
            self.stdout.write(self.style.SUCCESS(f"✅ Tenant '{tenant.nome}' deletado com sucesso."))

        except Cliente.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"❌ Nenhum tenant encontrado com schema '{schema_name}'."))
