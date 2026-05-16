from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.usuarios, name='user_page'),
    path('user_login/', views.userlogin, name='user_login'),
]