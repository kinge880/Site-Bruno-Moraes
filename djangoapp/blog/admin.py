from django.contrib import admin
from .models import Category, BlogPost
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Exibe os campos na lista de categorias
    search_fields = ('name',)  # Adiciona um campo de pesquisa pelo nome
    prepopulated_fields = {'slug': ('name',)}  # Preenche automaticamente o slug a partir do nome
    verbose_name = "Categoria"
    verbose_name_plural = "Categorias"

@admin.register(BlogPost) 
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'published_at', 'status', 'slug', 'image_preview', 'tags', 'categories_display'
    )
    list_filter = ('status', 'author', 'categories', 'published_at')
    search_fields = ('title', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-published_at',)
    verbose_name = "Postagem do blog"
    verbose_name_plural = "Postagens do blog"

    # Campos no formulário de edição, sem 'published_at'
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content', 'status', 'tags', 'categories', 'image')
        }),
    )

    # Visualização da imagem no admin
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image Preview'

    # Exibição das categorias na lista
    def categories_display(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    categories_display.short_description = 'Categories'