from django_cpf_cnpj.fields import CPFField, CNPJField
from django.db import models
from uuid import uuid4
from django.utils import timezone
from cloudinary.models import CloudinaryField



def upload_image_lente(instance,filename):
    return f"{instance.id_lente}-{filename}"

class DadosMedicao(models.Model):
    id_lente = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    OS = models.CharField(max_length=255,null=True,blank=True)
    horizontal = models.FloatField(null=True,blank=True)
    vertical = models.FloatField(null=True,blank=True)
    diagonal_maior = models.FloatField(null=True,blank=True)
    DNP = models.IntegerField(null=True,blank=True)
    altura = models.IntegerField(null=True,blank=True)
    leitura_direito = models.BooleanField(null=True,blank=True)
    leitura_esquerdo = models.BooleanField(null=True,blank=True)
    image = models.ImageField(upload_to=upload_image_lente, blank=True,null=True)
    image_cloud = CloudinaryField("image", blank=True,null=True)
    timestamp = models.DateTimeField(default=timezone.now, blank=True,null=True)
    cnpjOtica=CNPJField(masked=True, blank=True,null=True)
    cnpjLaboratorio = CNPJField(masked=True, blank=True,null=True)
    
    def __str__(self):
        return self.OS,self.cnpjOtica
    
    @property
    def image_url(self):
        return (
            f"https://res.cloudinary.com/diwsy7nll/{self.image}"
        )

