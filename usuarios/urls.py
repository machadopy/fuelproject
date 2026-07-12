from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.usuarios, name='user_page'),
    path('register/', views.register_view, name='register'),
    path('create/', views.register_create, name='register_create'),
    path('user_login/', views.user_login, name='user_login'),
    path('login_create/', views.login_create, name='login_create'),
    path('disparar/', views.disparar_mensagem, name='disparar_mensagem'),

]