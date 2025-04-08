from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

# Signal genérico para limpar cache
def invalidate_cache(sender, **kwargs):
    model_name = sender.__name__
    cache_keys = {
        'HomeBannerInicio': ['home_banners'],
        'HomeMinhaHistoria': ['home_historia'],
        'HomeBannerCampanha': ['home_banner_campanha'],
        'BlogPost': ['ultimas_postagens'],
        'PropostaProjetoLei': ['propostas_list'],
        'FaleComigo': ['contatos_recentes']
    }
    if model_name in cache_keys:
        for key in cache_keys[model_name]:
            cache.delete(key)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True, max_length=1000)
    adress = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outros')], blank=True, null=True)
    twitter = models.CharField(max_length=150, blank=True, null=True)
    face = models.CharField(max_length=150, blank=True, null=True)
    linkedin = models.CharField(max_length=150, blank=True, null=True)
    instagram = models.CharField(max_length=150, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) :
        return self.user.first_name + ' ' + self.user.last_name

class HomeBannerInicio(models.Model):
    titulo = models.CharField(blank = True, null = True, max_length = 250)
    subtitulo = models.CharField(blank = True, null = True, max_length = 200)
    imagem = models.ImageField(upload_to='home/banner/', blank=True, null=True)
    posicao = models.IntegerField(default = 1)
    
    def __str__(self):
        return str(self.posicao)

class HomeMinhaHistoria(models.Model):
    imagem = models.ImageField(upload_to='home/minhahist/')
    link = models.CharField(max_length=250)
    descricao = models.TextField(max_length=4000)
    
    def __str__(self):
        return str(self.link)

class HomeBannerCampanha(models.Model):
    imagemcampanha = models.ImageField(upload_to='home/minhahist/')
    link = models.CharField(max_length=250)
    
    def __str__(self):
        return str(self.link)

class Categoria(models.TextChoices):
    PROPOSTA = 'Proposta', 'Proposta'
    PROJETO = 'Projeto', 'Projeto'
    LEI = 'Lei', 'Lei'

class PropostaProjetoLei(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    pdf = models.FileField(upload_to='documentos/', blank=True, null=True)
    categoria = models.CharField(max_length=10, choices=Categoria.choices)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.titulo} ({self.categoria})"

class FaleComigo(models.Model):
    nome = models.CharField(max_length=100)  # Nome geralmente limitado a 100 caracteres
    email = models.EmailField(max_length=150)  # Emails podem ter até 150 caracteres
    telefone = models.CharField(max_length=20, blank=True, null=True)  # Formato internacional pode chegar a 20 caracteres
    descricao = models.TextField(max_length=15000)  # Reduzido para 5000 caracteres (evita carga desnecessária no BD)
    dtmov = models.DateTimeField(default=now)  # Define o padrão para a data atual
    visualizado = models.BooleanField(default=False)  # Adicionado um valor padrão

    def __str__(self):
        return f"{self.nome} - {self.email} ({'Lido' if self.visualizado else 'Não Lido'})"

# Registra os signals para todos os modelos
for model in [HomeBannerInicio, HomeMinhaHistoria, HomeBannerCampanha, PropostaProjetoLei, FaleComigo]:
    post_save.connect(invalidate_cache, sender=model)
    post_delete.connect(invalidate_cache, sender=model)