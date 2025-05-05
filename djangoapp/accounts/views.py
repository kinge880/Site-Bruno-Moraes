from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .forms import EmailAuthenticationForm
from django.shortcuts import redirect

class UsuarioLoginView(LoginView):
    template_name = 'accounts/registration/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')
    
def logout_view(request):
    logout(request)
    return redirect('/')