from django.urls import include, path
from fuelrequests import views
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


app_name='fuelrequests'

reembolsos_api_v2_router = SimpleRouter()
reembolsos_api_v2_router.register(
    'api/v2',
    views.ReembolsosApiv2Viewset,
    basename='reembolsos',
    )


urlpatterns = [
    path('', views.fuelrequests),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        
    path('', include(reembolsos_api_v2_router.urls)),
]