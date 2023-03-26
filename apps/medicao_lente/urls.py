from django.urls import include, path
from rest_framework import routers

from apps.medicao_lente.viewsets import DadosMedicaoViewSet

app_name = 'medicao_lente'

router = routers.DefaultRouter()
router.register(r'medicao', DadosMedicaoViewSet)

urlpatterns = [
    path(r'', include(router.urls)),

]
