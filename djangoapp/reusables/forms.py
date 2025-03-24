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
        fields = ['nome', 'email', 'telefone', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Digite seu nome',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Digite seu email',
                'required': True
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Digite seu telefone'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control bo-rad-10 size39 bo2 txt10',
                'placeholder': 'Escreva sua mensagem',
                'rows': 7,
                'required': True
            }),
        }