import urllib
import urllib.request
from pathlib import Path

import cv2
import numpy as np
from django.contrib.auth.models import User, Group
from django.core.files import File
from django.http import HttpResponse
from rest_framework import serializers

from apps.medicao_lente import measure_lens
from apps.medicao_lente.measure_lens import MeasurementLens
from apps.medicao_lente.models import DadosMedicao
from apps.usuarios.models import Usuarios

mlens = MeasurementLens()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DadosMedicaoSerializer(serializers.ModelSerializer):
    # horizontal = serializers.HiddenField(default=0)
    # vertical = serializers.HiddenField(default=0)
    # diagonalMaior = serializers.HiddenField(default=0)
    # OS = serializers.CharField(max_length=255)
    # DNP = serializers.IntegerField()
    # altura = serializers.IntegerField()
    # leituraDireito = serializers.BooleanField()
    # leituraEsquerdo = serializers.BooleanField()

    class Meta:
        model = DadosMedicao
        fields = "__all__"

    def create(self, validated_data):
        dado_medicao = DadosMedicao.objects.create(**validated_data)
        measure_lens.delay(id=dado_medicao.id.__str__())

        return dado_medicao

    # def create(self, validated_data):
    #     _medicao = DadosMedicao.objects.create(**validated_data)
    #     # measure_lens.delay(id=dado_medicao.id.__str__())
    #
    #     user = Usuarios.objects.get(email="andresjc2008@gmail.com")
    #
    #     os = DadosMedicao.objects.filter(OS=validated_data['OS']).exists()
    #
    #     if os is True:
    #         return "OS já cadastrada"
    #
    #     # medicao = {
    #     #     'dnp': int(dnp),
    #     #     'ponte': ponte,
    #     #     'lado': side,
    #     #     'OS': request.POST.get('OS'),
    #     #     'cnpj_otica': request.POST.get('cnpj_otica'),
    #     #     'cnpj_laboratorio': request.POST.get('cnpj_laboratorio'),
    #     #     'imagem_lente': request.FILES.get("image"),
    #     #     'criado_por': user
    #     # }
    #
    #     # _medicao = DadosMedicao.objects.create(**medicao)
    #
    #     side = validated_data['side']
    #     ponte = validated_data['ponte']
    #
    #     id_file_url = urllib.request.urlopen(_medicao.imagem_lente.url)
    #     id_file_cloudnary = np.asarray(
    #         bytearray(id_file_url.read()), dtype=np.uint8)
    #     _image = cv2.imdecode(id_file_cloudnary, cv2.IMREAD_GRAYSCALE)
    #     lens = mlens.run(image=_image, side=side)
    #
    #     if lens.get("erro") == 'Aruco not found':
    #         return HttpResponse(lens["erro"])
    #
    #     _medicao.horizontal = lens["values"]["horizontal"]
    #     _medicao.vertical = lens["values"]["vertical"]
    #     _medicao.diagonal = lens["values"]["diagonal"]
    #     _medicao.oma = lens["oma"]
    #     _medicao.processado = True
    #
    #     name = f"OS_{str(_medicao.OS)}_ID_{str(_medicao.id)}.vca"
    #
    #     os = f'JOB="{_medicao.OS}"\n'
    #
    #     dbl = f'DBL={ponte}\n'
    #
    #     with open(name, 'w', encoding='utf-8') as file:
    #         file.write(os)
    #         file.write(lens["oma"])
    #         file.write(dbl)
    #
    #     path = Path(name)
    #
    #     with path.open(mode="rb") as f:
    #         _medicao.oma_file = File(f, name=path.name)
    #         _medicao.save()
    #
    #     return _medicao
