import os
import uuid
from uuid import uuid4

from django.db import models
from django_cpf_cnpj.fields import CNPJField

from apps.usuarios.models import Usuarios


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
    resultado = f'images-lens/{basename.__str__()}{ext}'

    return resultado

def generate_uuid4_filename_txt(instance, filename):
    """
    Generates a uuid4 (random) filename, keeping file extension

    :param filename: Filename passed in. In the general case, this will
                     be provided by django-ckeditor's uploader.
    :return: Randomized filename in urn format.
    :rtype: str
    """
    discard, ext = os.path.splitext(filename)
    basename = uuid.uuid4()
    resultado = f'oma-lens/{basename.__str__()}{ext}'

    return resultado

class DadosMedicao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    OS = models.CharField(max_length=255, unique=True,null=True, blank=True)
    horizontal = models.FloatField(null=True, blank=True)
    vertical = models.FloatField(null=True, blank=True)
    diagonal = models.FloatField(null=True, blank=True)
    lado = models.CharField(max_length=100)
    imagem_lente = models.ImageField(upload_to=generate_uuid4_filename, blank=True, null=True)
    oma = models.TextField(null=True, blank=True)
    oma_file = models.FileField(upload_to="oma-lens/", null=True, blank=True)
    dnp = models.IntegerField(null=True, blank=True)
    ponte = models.IntegerField(null=True, blank=True)
    altura = models.IntegerField(null=True, blank=True)
    processado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    cnpj_otica = CNPJField(masked=True, blank=True, null=True)
    cnpj_laboratorio = CNPJField(masked=True, blank=True, null=True)
    criado_por = models.ForeignKey(Usuarios, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.OS

    class Meta:
        db_table = 'dados_medicao'
        ordering = ['-data_criacao']
