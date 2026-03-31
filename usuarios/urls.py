from django.urls import path
from . import views

urlpatterns = [
    path('', views.usuarios),
    path('userlogin/', views.userlogin),
]