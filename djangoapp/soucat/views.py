from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from reusables.views import defineNavLinks, validar_cpf, validar_rg, validar_telefone
from reusables.models import MeusLinks
from .models import  FormularioCurso
from .forms import FormularioCursoForm  # Importa os dois formulários
from reusables.forms import MeusLinksForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django_ratelimit.decorators import ratelimit
from django.contrib import messages

def social_links(type):
    
    if type == 'cat':
        social_links = [
            {
                'name': 'WhatsApp',
                'url': 'https://wa.me/556892577163?text=OI%2C+sou+terceirizado+e+quero+fazer+parte+do+CAT'
            }
        ]
        
        return {
            'main_color': '#FF6600',
            'social_links': social_links
        }
    elif type == 'fagner':
        social_links = [
            {
                'name': 'WhatsApp',
                'url': 'https://wa.me/556892577163?text=OI%2C+sou+terceirizado+e+quero+fazer+parte+do+CAT'
            }
        ]
        
        return {
            'main_color': '#FF6600',
            'social_links': social_links
        }
    
def land_home(request):
    context = defineNavLinks('homepage')
    context['main_color']  = social_links('cat')['main_color']
    context['social_links']  = social_links('cat')['social_links']
    
    context['links'] = MeusLinks.objects.all().filter(location_link='soucat')
    context['form'] = MeusLinksForm()
    context['curso_form'] = FormularioCursoForm()  # Adiciona o form de cursos
    context['location_link'] = 'soucat'
    context['linkcol'] = 'col-12 col-md-4'
    context['heigthcard'] = '450'
    
    if request.method == 'POST':
        # Aqui vamos verificar de onde veio o POST
        if 'salvar_link' in request.POST:
            form = MeusLinksForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('land_home')

    return render(request, 'home/land_page.html', context)

def politica_privacidade(request):
    return render(request, 'home/politica_privacidade.html')

def sobre_nos(request):
    return render(request, 'home/sobre_nos.html')

def termos_de_uso(request):
    return render(request, 'home/termos_de_uso.html')

@ratelimit(key='ip', rate='5/m', block=True)
def salvar_formulario_curso(request):
    if request.method == 'POST':
        form = FormularioCursoForm(request.POST)
        if form.is_valid():
            if not validar_cpf(form.cleaned_data['cpf']):
                messages.error(request, "CPF inválido.")
                return redirect('land_home')

            if not validar_rg(form.cleaned_data['rg']):
                messages.error(request, "RG inválido.")
                return redirect('land_home')

            formulario = FormularioCurso(
                nome_completo=form.cleaned_data['nome_completo'],
                cpf=form.cleaned_data['cpf'],
                rg=form.cleaned_data['rg'],
                telefone=form.cleaned_data['telefone'],
                data_nascimento=form.cleaned_data['data_nascimento'],
                rua=form.cleaned_data['rua'],
                cep=form.cleaned_data['cep'],
                bairro=form.cleaned_data['bairro'],
                numero=form.cleaned_data['numero'],
                cidade=form.cleaned_data['cidade'],
                estado=form.cleaned_data['estado'],
                sexo=form.cleaned_data['sexo'],
                funcionario_terceirizado=True if form.cleaned_data['funcionario_terceirizado'] == 'Sim' else False,
                filho_funcionario_terceirizado=True if form.cleaned_data['filho_funcionario_terceirizado'] == 'Sim' else False,
            )
            formulario.save()

            # Montar o conteúdo do e-mail usando template
            email_subject = f"Inscrição de {form.cleaned_data['nome_completo']} Recebida"
            email_recipient = ['apurinaagencia@gmail.com']  # Substitua pelo seu e-mail destino
            email_from = settings.DEFAULT_FROM_EMAIL

            email_body = render_to_string('emails/formulario_curso.html', {
                'formulario': formulario
            })

            send_mail(
                email_subject,
                '',
                email_from,
                email_recipient,
                html_message=email_body,
                fail_silently=False,
            )

            return redirect('formulario_sucesso')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
            
    return redirect('land_home')

def formulario_sucesso(request):
    return render(request, 'home/formulario_sucesso.html')