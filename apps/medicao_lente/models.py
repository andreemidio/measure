import os
import uuid
from uuid import uuid4

from django.db import models
from django_cpf_cnpj.fields import CNPJField


def upload_image_lente(instance, filename):
    return f"{instance.id_lente}-{filename}"


def generate_uuid4_filename(instance, filename):
    """
    Generates a uuid4 (random) filename, keeping file extension

    :param filename: Filename passed in. In the general case, this will
                     be provided by django-ckeditor's uploader.
    :return: Randomized filename in urn format.
    :rtype: str
    """
    discard, ext = os.path.splitext(filename)
    basename = uuid.uuid4()
    resultado = f'{basename.__str__()}{ext}'

    return resultado


class DadosMedicao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    OS = models.CharField(max_length=255, null=True, blank=True)
    horizontal = models.FloatField(null=True, blank=True)
    vertical = models.FloatField(null=True, blank=True)
    diagonalMaior = models.FloatField(null=True, blank=True)
    oma = models.TextField(null=True, blank=True)
    DNP = models.IntegerField(null=True, blank=True)
    ponte = models.IntegerField(null=True, blank=True)
    altura = models.IntegerField(null=True, blank=True)
    leituraDireito = models.BooleanField(null=True, blank=True)
    leituraEsquerdo = models.BooleanField(null=True, blank=True)
    image = models.ImageField(upload_to=generate_uuid4_filename, blank=True, null=True)
    dataCriacao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    cnpjOtica = CNPJField(masked=True, blank=True, null=True)
    cnpjLaboratorio = CNPJField(masked=True, blank=True, null=True)

    def __str__(self):
        return self.OS, self.cnpjOtica

    class Meta:
        db_table = 'dados_medicao'
        ordering = ['-dataCriacao']
