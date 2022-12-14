# Generated by Django 3.2.15 on 2022-12-02 19:34

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0015_alter_annex_internalcall_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentscall',
            name='active',
            field=models.BooleanField(default=True, help_text='Oculta la convoctaria de la vista pública', verbose_name='Convocatoria activa'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='economic_stimulus',
            field=models.CharField(help_text='ej. 3 pagos de $2.000.000 y uno de $350.000', max_length=4096, verbose_name='Estímulo económico'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='expiration',
            field=models.DateField(help_text='Hasta cuando está abierta la convocatoria', verbose_name='Finalización'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='funding',
            field=models.CharField(max_length=4096, verbose_name='Recursos del proyecto'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='period',
            field=models.CharField(help_text='ej. 3 Meses y 5 días', max_length=1024, verbose_name='Periodo'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='profile',
            field=tinymce.models.HTMLField(max_length=4096, verbose_name='Perfil'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='students',
            field=models.IntegerField(help_text='Cantidad de estudiantes en la convocatoria', verbose_name='Estudiantes'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='supervise',
            field=models.CharField(max_length=4096, verbose_name='Profesor responsable'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='time',
            field=models.IntegerField(help_text='Horas a la semana', verbose_name='Tiempo'),
        ),
        migrations.AlterField(
            model_name='studentscall',
            name='title',
            field=models.CharField(max_length=1024, verbose_name='Título'),
        ),
    ]
