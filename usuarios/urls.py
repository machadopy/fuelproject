from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = 'usuarios'

urlpatterns = [
    path('', views.UsuarioHome.as_view(), name='user_page'),
    path('register/', views.register_view, name='register'),
    path('create/', views.register_create, name='register_create'),
    path('user_login/', views.user_login, name='user_login'),
    path('login_create/', views.login_create, name='login_create'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/user_login'), name='logout'),
    path('disparar/', views.disparar_mensagem, name='disparar_mensagem'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<int:id>/', views.ProfileView.as_view(), name='profile'),

]