# Generated by Django 3.2.15 on 2022-08-11 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research_groups', '0002_researchgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchgroup',
            name='departament',
            field=models.CharField(choices=[('admin', 'Departamento de administración'), ('human', 'Departamento de ciencias humanas'), ('fisic', 'Departamento de física y química'), ('infor', 'Departamento de informática y computación'), ('civil', 'Departamento de ingeniería civil'), ('elect', 'Departamento de ingeniería eléctrica, electrónica y computación'), ('indus', 'Departamento de ingeniería industrial'), ('chemi', 'Departamento de ingeniería química'), ('maths', 'Departamento de matemáticas'), ('archi', 'Escuela de arquitectura y urbanismo')], max_length=5),
        ),
        migrations.AlterField(
            model_name='researchgroup',
            name='faculty',
            field=models.CharField(choices=[('admin', 'Facultad de administración'), ('exact', 'Facultad de ciencias excatas y naturales'), ('ingen', 'Facultad de ingeniería y arquitectura')], max_length=5),
        ),
        migrations.AlterField(
            model_name='researchgroup',
            name='ocde',
            field=models.CharField(choices=[('', 'Ciencias naturales'), ('', 'Ingeniería y tecnología'), ('', 'Ciencias médicas y de la salud'), ('', 'Ciencias agrícolas'), ('', 'Ciencias sociales'), ('', '')], max_length=2),
        ),
        migrations.AlterField(
            model_name='researchgroup',
            name='sub_ocde',
            field=models.CharField(choices=[('', ''), ('', ''), ('', ''), ('', ''), ('', '')], max_length=2),
        ),
    ]
