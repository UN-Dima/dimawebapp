# Generated by Django 4.1.2 on 2022-10-25 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_alter_researchgroup_researchers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchgroup',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
    ]
