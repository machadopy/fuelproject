from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.usuarios, name='user_page'),
    path('register/', views.register_view, name='register'),
    path('create/', views.register_created, name='create'),
    path('user_login/', views.userlogin, name='user_login'),
    path('disparar/', views.disparar_mensagem, name='disparar_mensagem'),

]