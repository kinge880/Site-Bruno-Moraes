from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Category, Comment
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator

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

    if request.user.is_authenticated:
        posts = BlogPost.objects.filter(status='published').annotate(comments_count=Count('comments'))
    else:
        posts = BlogPost.objects.all().annotate(comments_count=Count('comments'))
    
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

def blog_post_detail(request, categoria, slug):
    # Busca o post pelo slug
    category = get_object_or_404(Category, slug=categoria)
    post = get_object_or_404(BlogPost, slug=slug, categories=category)
    comments_list = Comment.objects.filter(post=post).order_by('-created_at')
    
    form = CommentForm()

    # Coletando dados para a sidebar
    sidebar_data = get_sidebar_data()

    return render(request, 'bloghome/detail_post.html', {
        'post': post,
        'comments': comments_list,
        'form': form,
        **sidebar_data,  # Passando os dados da sidebar para manter a consistência
    })

def get_comments(request, categoria, slug):
    category = get_object_or_404(Category, slug=categoria)
    post = get_object_or_404(BlogPost, slug=slug, categories=category)
    # Suponha que você tenha um modelo Comment
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    # Paginação de 10 comentários por vez
    paginator = Paginator(comments, 10)  # 10 comentários por página

    # Pega o número da página (caso seja a primeira vez, será 1)
    page = request.GET.get('page', 1)
    comments_page = paginator.get_page(page)

    # Crie um dicionário com os dados para retornar
    comment_list = []
    for comment in comments_page:
        liked_by_user = False
        if request.user.is_authenticated:
            liked_by_user = CommentLike.objects.filter(user=request.user, comment=comment).exists()
            
        comment_list.append({
            'id': comment.id,
            'name': comment.name,
            'created_at': str(naturaltime(comment.created_at)),
            'content': comment.content,
            'likes': comment.likes.count(),
            'can_delete': request.user == comment.user or request.user.is_superuser,
            'liked_by_user': liked_by_user,
            'authenticated': request.user.is_authenticated

        })

    return JsonResponse({
        'comments': comment_list,
        'has_next': comments_page.has_next()
    })
    
def post_comment(request, categoria, slug):
    category = get_object_or_404(Category, slug=categoria)
    post = get_object_or_404(BlogPost, slug=slug, categories=category)

    if request.method == "POST":
        # Verifique se o usuário está autenticado e forneça os valores de 'name' e 'email' conforme necessário
        name = request.user.username if request.user.is_authenticated else "Anônimo"
        
        if request.user.is_authenticated:
            name = request.user.username 
            form = CommentForm(request.POST, user=request.user)
        else:
            name = "Anônimo"
            form = CommentForm(request.POST)
        
        can_delete = request.user.is_authenticated and (request.user.is_staff or comment.user == request.user)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user if request.user.is_authenticated else None
            comment.save()

            # Se for uma requisição AJAX, retorna JSON com os dados do comentário
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    "success": True,
                    "name": name,
                    "content": comment.content,
                    'created_at': naturaltime(comment.created_at),
                    "likes": 0,
                    "can_delete": can_delete
                })

        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return redirect('blog_detail', categoria=categoria, slug=slug)

def like_comment(request, categoria, slug, comment_id):
    # Obtém o post pela categoria e slug
    category = get_object_or_404(Category, slug=categoria)
    post = get_object_or_404(BlogPost, slug=slug, categories=category)
    
    # Obtém o comentário
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    
    if request.user.is_authenticated:
        # Para usuários autenticados
        like_exists = CommentLike.objects.filter(comment=comment, user=request.user).exists()
        
        if like_exists:
            # Se já deu like, remove
            CommentLike.objects.filter(comment=comment, user=request.user).delete()
            action = 'removed'
        else:
            # Se não deu like, cria um novo like
            CommentLike.objects.create(comment=comment, user=request.user)
            action = 'added'
    else:
        # Para usuários não autenticados, usamos sessionStorage no frontend
        if not request.session.get(f'liked_comment_{comment_id}', False):
            request.session[f'liked_comment_{comment_id}'] = True
            # Incrementar o like, se necessário (isto não salva no banco, apenas no frontend)
            action = 'added'
        else:
            action = 'removed'
            request.session[f'liked_comment_{comment_id}'] = False
    
    # Redireciona de volta para a página do post
    return JsonResponse({'action': action, 'comment_id': comment_id})

@login_required(login_url='/login')
def delete_comment(request, categoria, slug, comment_id):
    category = get_object_or_404(Category, slug=categoria)
    post = get_object_or_404(BlogPost, slug=slug, categories=category)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        return JsonResponse({"success": True, "message": "Comentário excluído com sucesso!"})

    return JsonResponse({"success": False, "message": "Você não tem permissão para excluir este comentário."}, status=403)

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