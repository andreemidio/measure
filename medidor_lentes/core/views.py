from django.shortcuts import render
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import DadosMedicaoSerializer
from .models import DadosMedicao
from django_filters.rest_framework import DjangoFilterBackend
import numpy as np
import cv2 as cv
import io
from .filters import CnpjFilter
from .models import DadosMedicao
from rest_framework import generics
from rest_framework.filters import SearchFilter


class DadosMedicaoViewSet(viewsets.ModelViewSet):
    queryset = DadosMedicao.objects.all()
    serializer_class = DadosMedicaoSerializer
    permission_classes = permissions.AllowAny,


class CnpjList(viewsets.ModelViewSet):
    queryset = DadosMedicao.objects.all()
    serializer_class = DadosMedicaoSerializer

    def get_queryset(self):
        return self.queryset.all()

    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        cnpj_optica = self.request.query_params.get('cnpj_optica')
        os = self.request.query_params.get('os')
        cnpj_laboratorio = self.request.query_params.get('cnpj_laboratorio')
        #TODO criar combinação de pesquisas, os e lab, os e loja por exemplo
        if cnpj_optica:
            queryset = self.queryset.filter(cnpjOtica=cnpj_optica)
        elif os:
            queryset = self.queryset.filter(OS=os)

        elif cnpj_laboratorio:
            queryset = self.queryset.filter(cnpjLaboratorio=cnpj_laboratorio)

        serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data, status.HTTP_200_OK)
