from django.urls import path
from . import views

app_name = 'reembolsos'

urlpatterns = [
    path('', views.ReembolsosListViewBase.as_view(), name='reembolsos_all'),
    path('api/v1/', views.ReembolsosListApiv1.as_view(), name='reembolsos_all_apiv1'),

    
    path('search/', views.SearchListView.as_view(), name='search'),


    path('<int:pk>/',views.ReembolsosDetail.as_view(), name='detalhes_reembolsos'),
    path('api/v1/<int:pk>/',views.ReembolsosDetailApiv1.as_view(), name='detalhes_reembolsos_apiv1'),


    path('editar/<int:id>/', views.ReembolsoEdit.as_view(), name='editar_reembolsos'),
    path('deletar/<int:id>/', views.ReembolsoEdit.as_view(), name='deletar_reembolsos'),


    path('theory/', views.theory, name='theory'),
]