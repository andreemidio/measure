from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from medidor_lentes import views
from core.views import DadosMedicaoViewSet, CnpjList
from django.conf.urls.static import static
from django.conf import settings
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'core', DadosMedicaoViewSet)
router.register(r'cnpj', CnpjList)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include(router.urls)),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
