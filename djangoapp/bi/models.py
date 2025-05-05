from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='nomes')
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name='descrição')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BIReport(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(help_text='Resumo do que trata este BI')
    embed_url = models.URLField(help_text='Link para embed do BI', max_length=500)
    category = models.ForeignKey(
        Category,
        related_name='bi_reports',
        on_delete=models.PROTECT
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'BI Report'
        verbose_name_plural = 'BI Reports'
        ordering = ['title']
        unique_together = ('slug',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BIReport.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('dashboard:bi_detail', kwargs={'slug': self.slug})
