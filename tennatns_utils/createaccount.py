from customers.models import Cliente, Domain

# cliente mercale
nome = "Mercale"
schema_name = "mercale"
email_contato = "ti@mercale.com"
dominio = "mercale.localhost"

# Cria o tenant
tenant = Cliente.objects.create(
    nome=nome,
    schema_name=schema_name,
    email_contato=email_contato
)

# Cria o domínio
Domain.objects.create(
    domain=dominio,
    tenant=tenant,
    is_primary=True
)

print(f"✅ Cliente '{nome}' criado com domínio '{dominio}' e schema '{schema_name}'")


from customers.models import Cliente, Domain
# Recupera o tenant public
tenant = Cliente.objects.get(schema_name='public')

# Atualiza os dados
tenant.nome = "Admin"
tenant.email_contato = "admin@flowbi.com"
tenant.save()

# Cria ou atualiza o domínio
Domain.objects.update_or_create(
    domain="localhost",
    defaults={
        "tenant": tenant,
        "is_primary": True
    }
)

print("✅ Tenant 'public' nomeado como 'Admin' e domínio 'localhost' criado/atualizado com sucesso.")
