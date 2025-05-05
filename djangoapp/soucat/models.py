from django.db import models

class FormularioCurso(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Outros', 'Outros'),
    ]

    CURSO_CHOICES = [
        ('Informática Básica', 'Informática Básica'),
        ('Atendimento ao Cliente e Vendas', 'Atendimento ao Cliente e Vendas'),
        ('Comunicação Eficiente', 'Comunicação Eficiente'),
        ('Gestão de Tempo e Produtividade', 'Gestão de Tempo e Produtividade'),
        ('Empreendedorismo Social', 'Empreendedorismo Social'),
        ('Como se Destacar no Mercado de Trabalho', 'Como se Destacar no Mercado de Trabalho'),
        ('Marketing digital', 'Marketing digital'),
    ]

    nome_completo = models.CharField("Nome Completo", max_length=255)
    cpf = models.CharField("CPF", max_length=14)
    rg = models.CharField("RG", max_length=20)
    telefone = models.CharField("WhatsApp", max_length=15)
    data_nascimento = models.DateField("Data de Nascimento")
    rua = models.CharField("Rua", max_length=255)
    cep = models.CharField("CEP", max_length=9)
    bairro = models.CharField("Bairro", max_length=100)
    numero = models.CharField("Número", max_length=10)
    cidade = models.CharField("Cidade", max_length=100)
    estado = models.CharField("Estado", max_length=50)
    sexo = models.CharField("Sexo", max_length=20, choices=SEXO_CHOICES)
    funcionario_terceirizado = models.BooleanField("É Funcionário Terceirizado?")
    filho_funcionario_terceirizado = models.BooleanField("É Filho de Funcionário Terceirizado?")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)

    def __str__(self):
        return self.nome_completo
