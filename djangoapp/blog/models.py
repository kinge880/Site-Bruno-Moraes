from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import re

class Category(models.Model):
    name = models.CharField(max_length=70, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado')
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    excerpt = models.CharField(max_length=255, blank=True, help_text="Resumo ou introdução da postagem")
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255, blank=True, help_text="Separado por vírgulas")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        verbose_name = "Postagens do blog"
        verbose_name_plural = "Postagens do blog"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1

            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1

            self.slug = slug

        # Se o excerpt não for fornecido, gerar automaticamente a partir do início do conteúdo
        if not self.excerpt and self.content:
            self.excerpt = self.content[:255]  # Limita o resumo a 255 caracteres

        # Remove todas as tags HTML do conteúdo e do excerpt
        self.content = self.remove_html_tags(self.content)
        self.excerpt = self.remove_html_tags(self.excerpt)

        super().save(*args, **kwargs)

    def remove_html_tags(self, html_content):
        """Remove todas as tags HTML do conteúdo."""
        if not html_content:
            return html_content

        # Usando uma expressão regular para remover todas as tags HTML
        clean_content = re.sub(r'<.*?>', ' ', html_content)
        return clean_content

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.name} em {self.post.title}'