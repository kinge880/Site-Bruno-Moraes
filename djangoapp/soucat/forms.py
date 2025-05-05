from django import forms

class FormularioCursoForm(forms.Form):
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

    nome_completo = forms.CharField(
        label="Nome Completo",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'Nome Completo'
        })
    )

    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'CPF'
        })
    )

    rg = forms.CharField(
        label="RG",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'RG'
        })
    )

    telefone = forms.CharField(
        label="WhatsApp",
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'Telefone com WhatsApp'
        })
    )



    data_nascimento = forms.DateField(
        label="Data de Nascimento",
        widget=forms.DateInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'DD/MM/AAAA',
            'type': 'date'  # Deixa o input como date picker se possível
        })
    )

    rua = forms.CharField(
        label="Rua",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'Rua'
        })
    )

    cep = forms.CharField(
        label="CEP",
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'CEP'
        })
    )

    bairro = forms.CharField(
        label="Bairro",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'Bairro'
        })
    )

    numero = forms.CharField(
        label="Número",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'Número'
        })
    )

    cidade = forms.CharField(
        label="Cidade",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'Cidade'
        })
    )

    estado = forms.CharField(
        label="Estado",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
            'placeholder': 'Estado'
        })
    )

    sexo = forms.ChoiceField(
        label="Sexo",
        choices=SEXO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20'
        })
    )

    funcionario_terceirizado = forms.ChoiceField(
        label="É Funcionário Terceirizado?",
        choices=[('', 'É Funcionário Terceirizado?'), ('Sim', 'Sim'), ('Não', 'Não')],
        widget=forms.Select(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20'
        })
    )

    filho_funcionario_terceirizado = forms.ChoiceField(
        label="É Filho de Funcionário Terceirizado?",
        choices=[('', 'É Filho de Funcionário Terceirizado?'), ('Sim', 'Sim'), ('Não', 'Não')],
        widget=forms.Select(attrs={
            'class': 'form-control bo-rad-10 sizefull txt10 p-l-20'
        })
    )
