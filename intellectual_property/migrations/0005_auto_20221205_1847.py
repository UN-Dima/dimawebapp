# Generated by Django 3.2.15 on 2022-12-05 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intellectual_property', '0004_alter_patent_departament'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patent',
            options={'verbose_name': 'Patente'},
        ),
        migrations.AlterField(
            model_name='patent',
            name='co_ownership',
            field=models.CharField(help_text='Separados por coma (,)', max_length=1024, verbose_name='Cotitularidad'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='departament',
            field=models.CharField(choices=[('departament_0001', 'Departamento de Administración'), ('departament_0002', 'Departamento de Ciencias Humanas'), ('departament_0003', 'Departamento de Física y Química'), ('departament_0004', 'Departamento de Informática y Computación'), ('departament_0005', 'Departamento de Ingeniería Civil'), ('departament_0006', 'Departamento de Ingeniería Eléctrica, Electrónica y Computación'), ('departament_0007', 'Departamento de Ingeniería Industrial'), ('departament_0008', 'Departamento de Ingeniería Química'), ('departament_0009', 'Departamento de Matemáticas'), ('departament_0010', 'Escuela de Arquitectura y Urbanismo')], max_length=116, verbose_name='Departamento'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='filed',
            field=models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='Radicado'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='filling',
            field=models.DateField(default='django.utils.timezone.now', verbose_name='Fecha de presentación'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='grant',
            field=models.DateField(default='django.utils.timezone.now', verbose_name='Fecha de concesión'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='name',
            field=models.CharField(max_length=1024, verbose_name='Nombre de la patente'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='patent_type',
            field=models.CharField(choices=[('patent_type_0001', 'Patente de invención'), ('patent_type_0002', 'Patente modelo de utilidad')], max_length=116, verbose_name='Tipo de patente'),
        ),
        migrations.AlterField(
            model_name='patent',
            name='publication',
            field=models.DateField(default='django.utils.timezone.now', verbose_name='Fecha de publicación'),
        ),
    ]
