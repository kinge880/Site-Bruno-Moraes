from django import forms
from .models import *
from django.utils.safestring import mark_safe

class HomeBannerInicioForm(forms.ModelForm):
    class Meta:
        model = HomeBannerInicio
        fields = ['titulo', 'subtitulo', 'imagem', 'posicao']

class HomeMinhaHistoriaForm(forms.ModelForm):
    class Meta:
        model = HomeMinhaHistoria
        fields = ['imagem', 'link', 'descricao']
        widgets = {
            'imagem': forms.FileInput(attrs={'class': 'd-none image-upload-minhahist'}),
            'link': forms.TextInput(attrs={'class': 'form-control bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'URL do youtube'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control bo-rad-10 size39 bo2 txt10 d-none', 'placeholder': 'Digite toda história aqui'}),
        }

class HomeBannerCampanhaForm(forms.ModelForm):
    class Meta:
        model = HomeBannerCampanha
        fields = ['imagemcampanha', 'link']
        widgets = {
            'imagemcampanha': forms.FileInput(attrs={'class': 'd-none image-upload-banner-campanha'}),
            'link': forms.TextInput(attrs={'class': 'form-control bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'URL do youtube'})
        }
        
class PropostaProjetoLeiForm(forms.ModelForm):
    class Meta:
        model = PropostaProjetoLei
        fields = ['titulo', 'descricao', 'pdf', 'categoria']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20', 'placeholder': 'Título'}),
            'descricao': forms.HiddenInput(),
            'pdf': forms.FileInput(attrs={'class': ' form-control-file', 'placeholder': 'Anexe o arquivo aqui'}),
            'categoria': forms.Select(attrs={'class': 'bo-rad-10 sizefull txt10 p-l-20'})
        }

class FaleComigoForm(forms.ModelForm):

    class Meta:
        model = FaleComigo
        fields = [
            'nome', 'telefone', 'endereco', 'email',
            'descricao', 'informacoes_adicionais', 'imagem'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Escreva aqui o seu nome completo ok?'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'De preferência um número com WhatsApp :)'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'O endereço completo da sua residência'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Seu e-mail (opcional)'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control bo-rad-10 size39 bo2 txt10',
                'placeholder': ' Conta pra gente o que está acontecendo, com o máximo de detalhes possíveis.',
                'rows': 5
            }),
            'informacoes_adicionais': forms.Textarea(attrs={
                'class': 'form-control bo-rad-10 size39 bo2 txt10',
                'placeholder': 'Como o nome de alguém envolvido, outro endereço, ponto de referência, telefone adicional ou qualquer outro detalhe que possa nos ajudar.',
                'rows': 3
            }),
            'imagem': forms.FileInput(attrs={'class': 'd-none image-upload'}),
        }
    
class MeusLinksForm(forms.ModelForm):
    class Meta:
        model = MeusLinks
        fields = ['url', 'imagem', 'location_link']
        widgets = {
            'url': forms.URLInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Insira a url de destino',
                'required': True
            }),
            'imagem': forms.FileInput(attrs={'class': 'd-none image-upload'}),
            'location_link': forms.TextInput(attrs={
                'class': 'd-none'
            })
        }