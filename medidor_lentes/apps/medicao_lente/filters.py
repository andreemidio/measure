from django_filters import rest_framework as filters

from .models import DadosMedicao


class CnpjFilter(filters.FilterSet):
    cnpjOtica = filters.CharFilter(field_name='cnpjOtica', lookup_expr='icontains')
    OS = filters.CharFilter(field_name='OS', lookup_expr='icontains')

    class Meta:
        model = DadosMedicao
        fields = ('cnpjOtica', 'OS')
