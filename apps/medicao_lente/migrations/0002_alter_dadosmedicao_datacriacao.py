# Generated by Django 3.2.18 on 2023-03-26 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicao_lente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadosmedicao',
            name='dataCriacao',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
