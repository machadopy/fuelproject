from django.http import Http404
from django.shortcuts import redirect, render
from fuelrequests.models import Fuelrequests
from fuelrequests.forms import FuelReqForms
from .models import Usuario
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import RegisterForm

# Create your views here.
def usuarios(request):
        
        page_solicitacoes = Fuelrequests.objects.all().order_by('-data_solicitacao')[:9]
        return render(request, 'usuarios/index.html', {'page_solicitacoes':page_solicitacoes})


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


def register_created(request):
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

                messages.success(request, "Usuário cadastrado com sucesso!Faça login para continuar.")
                return redirect('usuarios:user_login') 
        else:
                request.session['register_form_data'] = POST
                return redirect('usuarios:register') 

def disparar_mensagem(request):

    return redirect(request, 'usuarios:user_page')

def userlogin(request):
        return render(request, 'usuarios/user_login.html')

