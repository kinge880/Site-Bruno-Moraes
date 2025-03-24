from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

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