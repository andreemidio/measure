from django.contrib.auth.models import User, Group
from rest_framework import serializers

from apps.medicao_lente.models import DadosMedicao


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class DadosMedicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosMedicao
        fields = "__all__"
