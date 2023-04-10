from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions

from apps.medicao_lente import views
from apps.medicao_lente.views import salvar_registro
from apps.medicao_lente.viewsets import DadosMedicaoViewSet, CnpjList

router = routers.DefaultRouter()

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

    path('', views.login_view, name='login'),
    path('obras/', salvar_registro, name='obras'),
    path('documentacao/1/', views.documentacao_1, name='documentacao-1'),
    path('documentacao/2/', views.documentacao_2, name='documentacao-2'),
    path('documentacao/3/', views.documentacao_3, name='documentacao-3'),
    path('documentacao/categorias/', views.documentacao_categorias, name='documentacao-categorias'),
    path('upload/', views.upload, name='upload'),

    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('api/v1/usuarios/', include('apps.usuarios.urls', namespace='usuarios')),
    path('api/v1/lentes/', include('apps.medicao_lente.urls', namespace='medicao_lente')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
