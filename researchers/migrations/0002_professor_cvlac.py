# Generated by Django 4.1.2 on 2022-10-25 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='cvlac',
            field=models.URLField(blank=True, null=True, verbose_name='CvLAC'),
        ),
    ]
