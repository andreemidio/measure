# Generated by Django 4.1.7 on 2023-03-25 04:46

import apps.medicao_lente.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicao_lente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadosmedicao',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.medicao_lente.models.upload_image_lente),
        ),
    ]
