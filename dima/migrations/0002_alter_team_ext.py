# Generated by Django 4.1.2 on 2022-10-25 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dima', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='ext',
            field=models.IntegerField(verbose_name='extention (separated by comma)'),
        ),
    ]
