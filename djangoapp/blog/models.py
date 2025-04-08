from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import re
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete

# Signal genérico para limpar cache
def invalidate_cache(sender, **kwargs):
    model_name = sender.__name__
    cache_keys = {
        'BlogPost': ['ultimas_postagens'],
    }
    if model_name in cache_keys:
        for key in cache_keys[model_name]:
            cache.delete(key)
            
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")  # Campo para associar usuário logado
    name = models.CharField(max_length=100, blank=True)  # Campo de nome (para usuários deslogados)
    email = models.EmailField(max_length=100, blank=True)  # Campo de email (para usuários deslogados)
    content = models.TextField(max_length=15000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'Comentário de {self.user.username} em {self.post.title}'
        return f'Comentário de {self.name} em {self.post.title}'

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')  # Impede múltiplos likes do mesmo usuário no mesmo comentário

    def __str__(self):
        return f'{self.user.username} curtiu o comentário {self.comment.id}'
    
# Registra os signals para todos os modelos
for model in [BlogPost]:
    post_save.connect(invalidate_cache, sender=model)
    post_delete.connect(invalidate_cache, sender=model)
