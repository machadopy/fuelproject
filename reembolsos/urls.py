from django.urls import path
from . import views

app_name = 'reembolsos'

urlpatterns = [
    path('', views.reembolsos, name='reembolsos_all'),
    path('search/', views.search, name='search'),
    path('<int:id>/',views.detalhes_reembolsos, name='detalhes_reembolsos'),
    path('editar/<int:id>/', views.editar_reembolsos, name='editar_reembolsos'),
    path('deletar/<int:id>/', views.deletar_reembolsos, name='deletar_reembolsos'),
]