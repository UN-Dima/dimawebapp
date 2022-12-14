# Generated by Django 3.2.15 on 2022-12-02 19:49

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0018_auto_20221202_1447'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='internalcall',
            options={'verbose_name': 'Convocatoria interna'},
        ),
        migrations.AlterField(
            model_name='internalcall',
            name='active',
            field=models.BooleanField(default=True, help_text='Oculta la convoctaria de la vista pública', verbose_name='Convocatoria activa'),
        ),
        migrations.AlterField(
            model_name='internalcall',
            name='objective',
            field=tinymce.models.HTMLField(max_length=4096, verbose_name='Objetivo'),
        ),
    ]
