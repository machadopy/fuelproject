from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse 
from fuelrequests.models import Fuelrequests
from fuelrequests.forms import FuelReqForms
from reembolsos.views.all import ReembolsosListViewBase
from usuarios.models import Usuario
from django.core.paginator import Paginator
from django.contrib import messages
from usuarios.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class UsuarioHome(LoginRequiredMixin, ReembolsosListViewBase):
        login_url = 'usuarios:user_login'
        redirect_field_name = 'next'
        template_name = 'usuarios/dashboard.html'


        def get_queryset(self, *args, **kwargs):
                qs = super().get_queryset(*args, **kwargs)
                if self.request.user.is_superuser:
                        return qs.order_by('-data_solicitacao')[:9]
                
                qs = qs.filter(usuario=self.request.user).order_by('-data_solicitacao')[:9]

                return qs

@login_required(login_url='usuarios:user_login', redirect_field_name='next')
def usuarios(request):
        
        if request.user.is_superuser:
                solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')[:9]
        else:
                solicitacoes = Fuelrequests.objects.filter(usuario=request.user)[:9]


        return render(request, 'usuarios/dashboard.html', {'page_solicitacoes':solicitacoes})


def register_view(request):
        request.session['number'] = request.session.get('number') or 1
        request.session['number'] +=1 
        
        register_form_data = request.session.get('register_form_data', None)
        form = RegisterForm(register_form_data)

        if register_form_data:
                form.is_valid()
                del request.session['register_form_data']

        context={
               'form': form,
        }
        return render(request, 'usuarios/register.html', context)


def register_create(request):
        if not request.POST:
                raise Http404
        
        POST = request.POST
        request.session['register_form_data'] = POST
        form = RegisterForm(POST)

        if form.is_valid():
                form.save()
                if 'register_form_data' in request.session:
                        del request.session['register_form_data']

                context={
                'form': form,
                }

                messages.success(request, "Usuário cadastrado com sucesso! Faça login para continuar.")
                return redirect('usuarios:user_login') 
        else:
                request.session['register_form_data'] = POST
                return redirect('usuarios:register') 

def disparar_mensagem(request):

    return redirect(request, 'usuarios:user_page')


def user_login(request):
        form = LoginForm()
        return render(request, 'usuarios/user_login.html', {
                'form': form,
                'form_action': reverse('usuarios:login_create')
        })


def login_create(request):
        if not request.POST:
                raise Http404
        
        form = LoginForm(request.POST)
        login_url = reverse('usuarios:dashboard')


        if form.is_valid():
                authenticated_user = authenticate(
                        username = form.cleaned_data.get('username',''),
                        password = form.cleaned_data.get('password', ''),
                        )
                
                if authenticated_user is not None:
                        messages.success(request, 'Login Realizado')
                        login(request, authenticated_user)
                else:
                        messages.error(request, 'Credenciais Inválidas')
        else:                
                messages.error(request, 'Erro ao validar campos')

        return redirect(login_url)
  
               
@login_required(login_url='usuarios:user_login', redirect_field_name='next')
def logout_views(request):
        if not request.POST:
                raise Http404
        
        if request.POST.get('username') != request.user.username:
                return redirect(reverse('usuarios:login'))

        logout(request)
        messages.warning(request, "Você saiu da sua conta com sucesso.")
        return redirect(reverse('usuarios:login'))


@login_required(login_url='usuarios:user_login', redirect_field_name='next')
def dashboard(request):
        
        if request.user.is_superuser:
                solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')[:9]
        else:
                solicitacoes = Fuelrequests.objects.filter(usuario=request.user)[:9]


        return render(request, 'usuarios/dashboard.html',{'page_solicitacoes':solicitacoes})

