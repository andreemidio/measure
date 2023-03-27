from django.urls import include, path
from rest_framework import routers

from apps.usuarios import views
from apps.usuarios.views import UserCreateViewSet

app_name = 'usuarios'

router = routers.DefaultRouter()

router.register(r'criar-usuario', UserCreateViewSet, basename='add')

urlpatterns = [
    path(r'', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token)

]
