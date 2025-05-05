from django.core.management.base import BaseCommand
from customers.models import Cliente, Domain
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Cria um novo tenant (cliente) com domínio primário'

    def handle(self, *args, **options):
        print("🔧 Criação de novo tenant FlowBi\n")

        nome = input("➡️ Nome do cliente: ").strip()
        schema_name = input("➡️ Nome do schema (ex: mercale): ").strip()
        email_contato = input("➡️ E-mail de contato: ").strip()

        dominio = input("➡️ Domínio principal (ex: mercale.localhost): ").strip().lower()

        if schema_name == "public":
            self.stderr.write(self.style.ERROR("❌ O schema 'public' é reservado. Escolha outro nome."))
            return

        if Cliente.objects.filter(schema_name=schema_name).exists():
            self.stderr.write(self.style.ERROR(f"❌ Já existe um schema '{schema_name}'"))
            return

        if Domain.objects.filter(domain=dominio).exists():
            self.stderr.write(self.style.ERROR(f"❌ O domínio '{dominio}' já está em uso"))
            return

        try:
            cliente = Cliente.objects.create(
                nome=nome,
                schema_name=schema_name,
                email_contato=email_contato
            )

            Domain.objects.create(
                domain=dominio,
                tenant=cliente,
                is_primary=True
            )

            self.stdout.write(self.style.SUCCESS(
                f"\n✅ Cliente '{nome}' criado com sucesso!"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"🌐 Domínio principal: http://{dominio}"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"🗂️ Schema: {schema_name}"
            ))
        except IntegrityError as e:
            self.stderr.write(self.style.ERROR(f"❌ Erro ao criar tenant: {e}"))
