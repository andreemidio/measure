from django.contrib.auth.models import User, Group
from rest_framework import serializers

from apps.medicao_lente.models import DadosMedicao
from apps.medicao_lente.tasks import measure_lens


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
