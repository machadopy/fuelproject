from django.urls import path
from fuelrequests import views

app_name='fuelrequests'

urlpatterns = [
    path('', views.fuelrequests),
    
    path('api/v2/', views.ReembolsosApiv2Viewset.as_view({'get':'list','post':'create'}), name='fuelreq_api_v2_list'),


    path('api/v2/<int:pk>/', views.ReembolsosApiv2Viewset.as_view({
        'get':'retrieve',
        'patch':'partial_update',
        'delete':'destroy'
    }
    ), name='fuelreq_api_v2_detail'),


]