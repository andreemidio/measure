from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from apps.medicao_lente.views import DadosMedicaoViewSet, CnpjList
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'medicao_lente', DadosMedicaoViewSet)
router.register(r'cnpj', CnpjList)

schema_view = get_schema_view(
    openapi.Info(
        title="Medição Lentes API",
        default_version='v1',
        description="Medição de lentes",
        terms_of_service="No terms",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="No License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

                  path('admin/', admin.site.urls),
                  # path('', include(router.urls)),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('', lambda request: redirect('docs/', permanent=True)),

                  path('camera/', include('apps.medicao_lente.urls', namespace='medicao_lente')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
