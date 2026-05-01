from django.urls import path
from . import views

app_name = 'reembolsos'

urlpatterns = [
    path('', views.reembolsos),
    path('search/', views.search, name='search'),
    path('<int:id>/',views.detalhes_reembolsos, name= 'detalhes_reembolsos'),
]