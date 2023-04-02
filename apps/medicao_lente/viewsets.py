from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication
from rest_framework import parsers
from rest_framework import permissions, viewsets, status
from rest_framework import renderers
from rest_framework.response import Response

from .measure_lens import MeasurementLens
# from .serializers import DadosMedicaoSerializer
from .models import DadosMedicao
from .serializers import DadosMedicaoSerializer

mlens = MeasurementLens()


class DadosMedicaoViewSet(viewsets.ModelViewSet):
    queryset = DadosMedicao.objects.all()
    serializer_class = DadosMedicaoSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['OS', 'cnpjOtica', 'cnpjLaboratorio']
    search_fields = ['OS', 'cnpjOtica', 'cnpjLaboratorio']
    parser_classes = [parsers.MultiPartParser]
    renderer_classes = [renderers.StaticHTMLRenderer, renderers.TemplateHTMLRenderer,
                        renderers.HTMLFormRenderer, renderers.JSONRenderer, ]



class CnpjList(viewsets.ModelViewSet):
    queryset = DadosMedicao.objects.all()

    # serializer_class = DadosMedicaoSerializer

    def get_queryset(self):
        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        cnpj_optica = self.request.query_params.get('cnpj_optica')
        os = self.request.query_params.get('os')
        cnpj_laboratorio = self.request.query_params.get('cnpj_laboratorio')
        # TODO criar combinação de pesquisas, os e lab, os e loja por exemplo
        if cnpj_optica:
            queryset = self.queryset.filter(cnpjOtica=cnpj_optica)
        elif os:
            queryset = self.queryset.filter(OS=os)

        elif cnpj_laboratorio:
            queryset = self.queryset.filter(cnpjLaboratorio=cnpj_laboratorio)

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
