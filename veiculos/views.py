from django.shortcuts import render

# Create your views here.
def veiculos(request):
    return render(request, 'veiculos/veiculos.html')