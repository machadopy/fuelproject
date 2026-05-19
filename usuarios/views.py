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
        
        register_form_data = request.session.get('register_form_data', None)
        form = RegisterForm(register_form_data)
        context={
               'form': form,
               'request_session': request.session['number']
        }
        return render(request, 'usuarios/register.html', context)


def register_created(request):
        if not request.POST:
                raise Http404
        
        POST = request.POST
        request.session['register_form_data'] = POST
        form = RegisterForm(POST)

        context={
               'form': form,
        }
        return redirect('usuarios:register')


def disparar_mensagem(request):

    return redirect(request, 'usuarios:user_page')

def userlogin(request):
        return render(request, 'usuarios/user_login.html')

