from django.shortcuts import render
import json
from django.apps import apps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as loginDjango
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.conf import settings
from project import conexao_postgresql
from .models import *
from .forms import *
from .ploty import *
from blog.models import *
from project.conexao_postgresql import *
import re
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests

def is_strong_password(password):
    length_weight = 0.15
    uppercase_weight = 0.5
    lowercase_weight = 0.5
    number_weight = 0.7
    symbol_weight = 1

    strength = 0

    # Calculate the strength based on the password length
    strength += len(password) * length_weight

    # Calculate the strength based on uppercase letters
    if any(c.isupper() for c in password):
        strength += uppercase_weight

    # Calculate the strength based on lowercase letters
    if any(c.islower() for c in password):
        strength += lowercase_weight

    # Calculate the strength based on numbers
    if any(c.isdigit() for c in password):
        strength += number_weight

    # Calculate the strength based on symbols
    if re.search(r'[!@#$%^&*()\-_=+{};:,<.>]', password):
        strength += symbol_weight

    return strength >= 4  # Retorna True se a força for 4 ou mais, False caso contrário

def get_instagram_profile():
    # Buscando informações do perfil, incluindo profile_picture_url, username e media_count.
    url = f"https://graph.instagram.com/me?fields=id,username,profile_picture_url,media_count&access_token={settings.INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

def get_instagram_posts():
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,permalink,like_count,comments_count&limit=8&access_token={settings.INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

def extrair_youtube_id(link):
    """
    Extrai o ID do vídeo de qualquer link válido do YouTube e retorna no formato embed.
    """
    # Padrão que captura qualquer formato de link do YouTube
    pattern = re.search(
        r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|shorts/|live/|user/.*?/|channel/.*?/|@.*?/)?|youtu\.be/)([a-zA-Z0-9_-]{11})',
        link
    )

    # Se encontrou um ID válido, retorna no formato embed
    if pattern:
        print('search')
        video_id = pattern.group(1)
        print(video_id)
        return f"https://www.youtube.com/embed/{video_id}"

    return None  # Se não for um link válido do YouTube


#metodo para obter as permissões de todo o app
def obterPermissao(request, id, valorperm):
    conexao = conexao_postgresql.conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(f'''
        SELECT idpermissao, valor, iduser
        FROM permissaoitem 
        WHERE 
            idpermissao = {id} AND
            valor = {valorperm} and 
            iduser = {request.user.id}
    ''')
    permissao = cursor.fetchone()

    return permissao

def defineNavLinks(value):
    if value == 'homepage':
        navbar_links = {
            'inicio': 'Início',
            'menu': 'Página do menu principal',
            'fixed': 'S'
        }

    elif value == 'menu_fixo':
        navbar_links = {
            'inicio': 'Início',
            'cadastro': 'cadastro',
            'processamento': 'processamento',
            'fixed': 'N'
        }
    else:
        navbar_links = {'fixed': 'N'}
    
    return navbar_links

def basehome(request):
    context = defineNavLinks('homepage')
    ultimas_postagens = BlogPost.objects.order_by('-published_at')[:3]
    
    print(ultimas_postagens)
    context['ultimas_postagens'] = ultimas_postagens
    context['banners_inicio'] = HomeBannerInicio.objects.all().order_by('posicao')

    # Verifica se já existe uma história salva e carrega no formulário
    historia = HomeMinhaHistoria.objects.last()
    if historia:
        form = HomeMinhaHistoriaForm(instance=historia)  # Preenche o formulário com a última história
    else:
        form = HomeMinhaHistoriaForm()  # Cria um novo formulário em branco, se não houver história
    
    banner = HomeBannerCampanha.objects.last()
    if banner:
        formBanner = HomeBannerCampanhaForm(instance=banner)  # Preenche o formulário com a última história
    else:
        formBanner = HomeBannerCampanhaForm()  # Cria um novo formulário em branco, se não houver história

    context['banner_campanha'] = banner
    context['formBanner'] = formBanner  # Passa o formulário preenchido para o template
    context['historia'] = historia  # Passa a última história para o template
    context['formMinhaHist'] = form  # Passa o formulário preenchido para o template

    context['posts'] = get_instagram_posts()          # Retorna a lista de posts
    context['profile'] = get_instagram_profile()
    return render(request, 'home/homePage.html', context)

@login_required(login_url='/login')
def basehome_edit(request):
    """ View responsável por exibir a página inicial com os banners e a última história salva. """
    context = defineNavLinks('homepage')
    context['banners_inicio'] = HomeBannerInicio.objects.all().order_by('posicao')

    # Verifica se já existe uma história salva e carrega no formulário
    historia = HomeMinhaHistoria.objects.last()
    if historia:
        form = HomeMinhaHistoriaForm(instance=historia)  # Preenche o formulário com a última história
    else:
        form = HomeMinhaHistoriaForm()  # Cria um novo formulário em branco, se não houver história

    context['historia'] = historia  # Passa a última história para o template
    context['formMinhaHist'] = form  # Passa o formulário preenchido para o template

    return render(request, 'home/homePage.html', context)

#Anonymous required 
def anonymous_required(function=None, redirect_url='/'):

    if not redirect_url:
        redirect_url = settings.LOGIN_REDIRECT_URL

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

#controles de login e cadastro de usuário
@anonymous_required
def login(request):
    
    if request.method == 'POST' :
        usuario = request.POST.get("username")
        senha = request.POST.get("password")
        
        user = authenticate(username=usuario, password=senha)

        if user:
            loginDjango(request, user)
            return redirect('/')
        else:
            messages.error(request, f'Nome de usuário ou senha incorretos!')
            return render(request, 'accounts/login.html')
    else:
        return render(request, 'accounts/login.html', {'login': 'login'})

@anonymous_required
def register(request):
    if not request.user.is_authenticated:
        if(request.method == "POST"):
            try:
                user_aux_email = User.objects.get(email=request.POST.get('email').strip())
                print(user_aux_email.username)
                if user_aux_email:
                    messages.error(request, f'Já existe um usuário cadastrado com o email informado')
                    return render(request, 'accounts/register.html')
            except User.DoesNotExist:
                try:
                    user_aux_username = User.objects.get(
                        username=request.POST.get('username').strip())
                    if user_aux_username:
                        messages.error(request, f'Usuário já cadastrado no sistema')
                        return render(request, 'accounts/register.html')
                except User.DoesNotExist:
                    user_parts = request.POST.get('fullname').strip().split(' ', 1)
                    user_first_name = user_parts[0]
                    user_last_name = user_parts[1] if len(user_parts) > 1 else ''
                    print(user_parts)

                    user_email = request.POST.get('email').strip()
                    user_login = request.POST.get('username').strip()
                    user_password = request.POST.get('password').strip()
                    user_phone_number= request.POST.get('phone', ' ').strip()

                    newUser = User.objects.create_user(email=user_email,
                                                        first_name=user_first_name,
                                                        last_name=user_last_name,
                                                        username=user_login,
                                                        password=user_password)
                    newUser.save()
                        
                    teste = User.objects.get(username=user_login)
                    newProfile = Profile.objects.create(user=teste,
                                                        phone = user_phone_number)

                    newProfile.save()
                    messages.success(request, f'Cadastro realizado com sucesso! Vamos logar :)')
                    return redirect('/login')
        else: 
            return render(request, 'accounts/register.html', {'cadastro': 'cadastro'})
    else: 
        return redirect('/')
    
def logout_view(request):
    logout(request)

    return redirect('/')

@login_required(login_url='/login')
def cadastrar_banner_inicio(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '')
        subtitulo = request.POST.get('subtitulo', '')
        imagem = request.FILES.get('imagem', None)
        posicao = request.POST.get('posicao', 1)

        novo_banner = HomeBannerInicio.objects.create(
            titulo=titulo,
            subtitulo=subtitulo,
            imagem=imagem,
            posicao=int(posicao)
        )

        placeholder = novo_banner.imagem.url if novo_banner.imagem else "https://placehold.co/1366x664"
        nova_linha = f'''
        <tr data-id="{novo_banner.id}" class="sortable-item">
            <td class="drag-handle ui-sortable-handle">☰</td>
            <td>{novo_banner.posicao}</td>
            <td>
                <div class=" size12 bo2 bo-rad-10 m-t-3 m-b-23">
                    <input type="text" name="titulo" class="bo-rad-10 sizefull txt10 p-l-20 update-field" value="{novo_banner.titulo}">
                </div>
            </td>
            <td>
                <div class=" size12 bo2 bo-rad-10 m-t-3 m-b-23">
                    <input type="text" name="subtitulo" class="bo-rad-10 sizefull txt10 p-l-20 update-field" value="{novo_banner.subtitulo}">
                </div>
            </td>
            <td>
                <input type="file" class="form-control image-upload" name="imagem" accept="image/*" style="display:none;">
                <img src="{placeholder}" class="img-thumbnail preview-image" width="100" style="cursor:pointer; max-height:55px !important;">
            </td>
            <td><button type="button" class="btn btn-danger remove-banner">X</button></td>
        </tr>
        '''

        return JsonResponse({'success': True, 'nova_linha': nova_linha})
    
    return JsonResponse({'success': False, 'message': 'Erro ao cadastrar banner'})

@login_required(login_url='/login')
def deletar_banner_inicio(request, banner_id):
    if request.method == 'POST':
        banner = get_object_or_404(HomeBannerInicio, id=banner_id)
        banner.delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Erro ao deletar banner'})

@login_required(login_url='/login')
def atualizar_banner_inicio(request, banner_id):
    if request.method == 'POST':
        field = request.POST.get('field')
        value = request.POST.get('value')
        if field != 'posicao':
            banner = get_object_or_404(HomeBannerInicio, id=banner_id)
        
        if field == 'titulo':
            banner.titulo = value
        elif field == 'subtitulo':
            banner.subtitulo = value
        elif field == 'imagem':
            imagem = request.FILES.get('imagem')
            if imagem:
                banner.imagem = imagem
        elif field == 'posicao':
            try:
                posicoes = request.POST.getlist('posicoes[]')  # Recebe a lista com todos os IDs dos banners ordenados
                for index, banner_id in enumerate(posicoes, start=1):
                    # Atualiza a posição de cada banner conforme a ordem
                    HomeBannerInicio.objects.filter(id=banner_id).update(posicao=index)
                return JsonResponse({'success': True, 'message': 'Ordem atualizada com sucesso'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Erro ao atualizar ordem: {str(e)}'})
            
        banner.save()
        return JsonResponse({'success': True, 'nova_imagem': banner.imagem.url if banner.imagem else ''})

    return JsonResponse({'success': False, 'message': 'Erro ao atualizar banner'})

def listar_banners(request):
    banners = HomeBannerInicio.objects.order_by("posicao").values("id", "titulo", "subtitulo", "imagem")
    return JsonResponse({"banners": list(banners)})

@login_required(login_url='/login')
def post_minha_historia(request):
    """ View separada para tratar POST de envio da história. """
    if request.method == 'POST':
        form = HomeMinhaHistoriaForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.cleaned_data.get("link")
            if link:
                novo_link = extrair_youtube_id(link)
                print(novo_link)
                form.cleaned_data["link"] = novo_link  # Atuliza o link
                if not novo_link:
                    messages.error(request, "O link do YouTube é inválido. Use um link válido do formato 'https://www.youtube.com/watch?v=ID'.")
                    return redirect('paginicial')
                
                # Apaga qualquer registro existente
                HomeMinhaHistoria.objects.all().delete()

                # Cria a instância do modelo e salva
                historia = form.save(commit=False)  # Cria o objeto, mas não salva ainda
                historia.link = novo_link  # Atualiza o campo "link"
                historia.save()  # Agora salva no banco

                messages.success(request, "História salva com sucesso!")
            else:
                messages.error(request, "Link informado é invalido, busque um link válido do youtube")
                return redirect('paginicial')
        else:
            # Monta uma mensagem com os erros específicos dos campos
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")

            messages.error(request, "Erro ao salvar! Verifique os campos e tente novamente. " + " | ".join(error_messages))
    else:
        messages.warning(request, "Método inválido. Somente POST é permitido.")
    
    return redirect('paginicial')  # Redireciona de volta após o POST

@login_required(login_url='/login')
def post_banner_campanha(request):
    """ View separada para tratar POST de envio da história. """
    if request.method == 'POST':
        form = HomeBannerCampanhaForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.cleaned_data.get("link")
            if link:
                novo_link = extrair_youtube_id(link)
                print(novo_link)
                form.cleaned_data["link"] = novo_link  # Atuliza o link
                if not novo_link:
                    messages.error(request, "O link do YouTube é inválido. Use um link válido do formato 'https://www.youtube.com/watch?v=ID'.")
                    return redirect('paginicial')
                
                # Apaga qualquer registro existente
                HomeBannerCampanha.objects.all().delete()

                # Cria a instância do modelo e salva
                banner = form.save(commit=False)  # Cria o objeto, mas não salva ainda
                banner.link = novo_link  # Atualiza o campo "link"
                banner.save()  # Agora salva no banco

                messages.success(request, "Banner e vídeo de campanha salvos com sucesso!")
            else:
                messages.error(request, "Link informado é invalido, busque um link válido do youtube")
                return redirect('paginicial')
        else:
            # Monta uma mensagem com os erros específicos dos campos
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")

            messages.error(request, "Erro ao salvar! Verifique os campos e tente novamente. " + " | ".join(error_messages))
    else:
        messages.warning(request, "Método inválido. Somente POST é permitido.")
    
    return redirect('paginicial')  # Redireciona de volta após o POST


def listar_propostas(request):
    propostas = PropostaProjetoLei.objects.filter(categoria='Proposta').order_by('-criado_em')
    projetos = PropostaProjetoLei.objects.filter(categoria='Projeto').order_by('-criado_em')
    leis = PropostaProjetoLei.objects.filter(categoria='Lei').order_by('-criado_em')
    
    form = PropostaProjetoLeiForm()
    
    context = defineNavLinks('menu_fixo')
    context['propostas'] = propostas
    context['projetos'] = projetos
    context['leis'] = leis
    context['form'] = form
    return render(request, 'propostas/propostas.html', context)

@login_required(login_url='/login')
def cadastrar_proposta(request):
    if request.method == 'POST':
        form = PropostaProjetoLeiForm(request.POST, request.FILES)
        if form.is_valid():
            proposta = form.save(commit=False)
            proposta.criado_por = request.user
            proposta.save()
            return redirect('listar_propostas')
    else:
        form = PropostaProjetoLeiForm()
    
    return render(request, 'propostas/modal_cadastro.html', {'form': form})

@login_required(login_url='/login')
def deletar_proposta(request, id):
    proposta = get_object_or_404(PropostaProjetoLei, id=id)
    if request.method == 'POST':
        proposta.delete()
        return redirect('listar_propostas')
    
def fale_comigo(request):
    context = defineNavLinks('menu_fixo')
    if request.method == "POST":
        form = FaleComigoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect('fale_comigo')  
        else:
            messages.error(request, "Erro ao enviar a mensagem. Verifique os dados informados.")
    else:
        form = FaleComigoForm()
        context['form'] = form
    
    return render(request, 'faleconosco/formulario.html', context)

def sobre_mim(request):
    context = defineNavLinks('menu_fixo')
    return render(request, 'sobre_mim/sobre_mim.html', context)

def webhook(request):
    verify_token = "MEU_TOKGHGHFGFHEN_SFGHGHECRETOGFGHFGH_123FGHFH"  # Defina um token para verificação

    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return HttpResponse(challenge, content_type="text/plain")
        else:
            return HttpResponse("Token inválido", status=403)
    
    return HttpResponse("Método não permitido", status=405)

def esportes(request):
    context = defineNavLinks('menu_fixo')
    return render(request, 'bandeiras/esportes.html', context)