from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Digite seu nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Digite seu e-mail'
            }),
            'content': forms.TextInput(attrs={
                'class': 'input-search-sidebar2 txt10 p-l-20 p-r-55',
                'placeholder': 'Escreva o seu comentário aqui'
            }),
        }

    def __init__(self, *args, **kwargs):
        # Se o usuário estiver logado, preenche automaticamente os campos de nome e e-mail
        if 'user' in kwargs:
            user = kwargs.pop('user')
            initial_data = kwargs.get('initial', {})
            initial_data['name'] = user.username
            initial_data['email'] = user.email
            kwargs['initial'] = initial_data

        super().__init__(*args, **kwargs)

        # Se o formulário não for preenchido por um usuário logado, os campos de nome e e-mail são obrigatórios
        if not self.instance.pk:  # Se a instância não for uma edição
            self.fields['name'].required = True
            self.fields['email'].required = True
        else:
            self.fields['name'].required = False
            self.fields['email'].required = False

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image', 'categories', 'tags', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Título da postagem'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bo-rad-10 size39 bo2 txt10 d-none',
                'placeholder': 'Escreva o texto da postagem aqui'
            }),
            'image': forms.FileInput(attrs={
                'class': 'd-none image-upload-blog'
            }),
            'categories': forms.Select(attrs={
                'class': 'form-control bo2'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control bo-rad-10 sizefull txt10 p-l-20',
                'placeholder': 'Digite quantas tags quiser, separadas por vírgulas'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control bo2'
            }),
        }