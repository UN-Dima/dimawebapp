# Generated by Django 4.2 on 2023-07-19 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dima', '0013_alter_attachment_content_attachment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment_content',
            name='area',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Área'),
        ),
        migrations.AddField(
            model_name='attachment_content',
            name='size',
            field=models.FloatField(blank=True, null=True, verbose_name='Tamaño'),
        ),
        migrations.AddField(
            model_name='attachment_content',
            name='tipo',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='attachment_content',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='uploads\\content', verbose_name='Adjunto'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='image',
            field=models.FileField(upload_to='uploads\\broadcast', verbose_name='Imagen para difusión'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='file',
            field=models.FileField(upload_to='uploads\\newsletter', verbose_name='Boletín'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='uploads\\newsletter'),
        ),
    ]
