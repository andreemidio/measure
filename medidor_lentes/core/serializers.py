from .models import DadosMedicao
from rest_framework import serializers

import cv2
import numpy as np
from .measure_lens import MeasurementLens

mlens = MeasurementLens()


class DadosMedicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosMedicao
        fields = "__all__"

    def create(self, validated_data):
        data = validated_data.get('image').read()
        _image = np.asarray(bytearray(data), dtype='uint8')
        _image = cv2.imdecode(_image, cv2.IMREAD_GRAYSCALE)

        lens = mlens.run(image=_image)

        validated_data["horizontal"] = lens["horizontal"]
        validated_data["vertical"] = lens["vertical"]
        validated_data["diagonal_maior"] = lens["diagonal_maior"]

        dado_medicao = DadosMedicao.objects.create(**validated_data)

        return dado_medicao
