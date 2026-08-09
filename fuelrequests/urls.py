from django.urls import path
from fuelrequests import views

app_name='fuelrequests'

urlpatterns = [
    path('', views.fuelrequests),
    path('api/v2/', views.ReembolsosAPIV2list.as_view(), name='fuelreq_api_v2_list'),

    path('api/v2/<int:pk>/', views.ReembolsosAPIV2detail.as_view(), name='fuelreq_api_v2_detail'),
    path('api/v2/tag/<int:pk>', views.tag_api_detail, name='fuelreq_api_v2_tag'),

    #path('api/v3/', views.reembolsos_listv3, name='fuelreq_api_v3'),

]