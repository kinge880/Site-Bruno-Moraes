from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Category, Comment
from django.http import HttpResponseRedirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth, ExtractYear
import calendar

def get_sidebar_data():
    # Coletando categorias com contagem de postagens
    categorias = (
        Category.objects
        .annotate(post_count=Count('blogpost', filter=Q(blogpost__status='published')))
        .order_by('-id')  # Opcional: ordena pela quantidade de postagens
    )

    # Coletando arquivos (agrupar por ano/mês)
    arquivos = (
        BlogPost.objects
        .filter(status='published')
        .annotate(year=ExtractYear('published_at'), month=ExtractMonth('published_at'))
        .values('year', 'month')
        .annotate(count=Count('id'))
        .order_by('-year', '-month')
    )

    # Traduzindo os meses para português
    meses_ptbr = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }

    for arq in arquivos:
        arq['month_name'] = meses_ptbr.get(arq['month'], "Mês desconhecido")

    return {
        'categorias': categorias,
        'arquivos': arquivos,
    }
    
def index(request, categoria=None, year=None, month=None):
    search_query = request.GET.get('search', '')

    posts = BlogPost.objects.filter(status='published').annotate(comments_count=Count('comments'))

    # Aplicando busca
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )

    # Filtro de categoria
    if categoria:
        posts = posts.filter(categories__slug=categoria)

    # Filtro de arquivo (ano/mês)
    if year and month:
        posts = posts.filter(published_at__year=year, published_at__month=month)

    # Coletando os dados da sidebar
    sidebar_data = get_sidebar_data()

    return render(request, 'bloghome/homeblog.html', {
        'posts': posts,
        'search_query': search_query,
        **sidebar_data,  # Aqui estamos passando os dados da sidebar
    })

def post_detail(request, categoria, slug):
    # Obtém o post com base no slug
    post = get_object_or_404(BlogPost, categories__slug = categoria, slug=slug)
    
    # Criação de formulário de comentário
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'form': form})

@login_required(login_url='/login')
def create_blog_post(request):
    # Coletando dados para a sidebar
    sidebar_data = get_sidebar_data()

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user  # Atribui o autor automaticamente
            blog_post.save()  # Salva a postagem

            messages.success(request, 'Postagem criada com sucesso!')
            return redirect('base_blog')  # Redireciona para a página principal do blog
        else:
            # Exibir mensagens de erro de forma mais amigável
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo '{field.capitalize()}': {error}")
    
    else:
        form = BlogPostForm()

    return render(request, 'bloghome/create_post.html', {
        'form': form,
        **sidebar_data,  # Passando os dados da sidebar
    })