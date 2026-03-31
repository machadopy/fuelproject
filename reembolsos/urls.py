from django.urls import path
from . import views

urlpatterns = [
    path('', views.reembolsos),
    path('<int:id>/',views.detalhes_reembolsos, name= 'detalhes_reembolsos')
]