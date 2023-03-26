from rest_framework import serializers

from apps.usuarios.models import Usuarios


class UsuariosCreateSerializer(serializers.ModelSerializer):
    # fullname = serializers.CharField(max_length=255)
    # cellphone = serializers.CharField(max_length=30)
    # email = serializers.EmailField()
    # password = serializers.CharField(max_length=16)

    # confirm_password = serializers.CharField(max_length=16)

    class Meta:
        model = Usuarios
        fields = '__all__'
        # fields = ['fullname', 'cellphone', 'email', 'password'
        #           # , 'confirm_password'
        #           ]

    def create(self, validated_data):
        validated_data.pop('password')
        # validated_data.pop('confirm_password')
        return super(UsuariosCreateSerializer, self).create(validated_data)
