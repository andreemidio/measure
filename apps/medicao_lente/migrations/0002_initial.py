# Generated by Django 4.2.1 on 2023-06-19 11:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medicao_lente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosmedicao',
            name='criado_por',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]