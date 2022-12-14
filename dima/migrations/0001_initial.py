# Generated by Django 4.1.2 on 2022-10-18 14:05

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Broadcast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='uploads/broadcast', verbose_name='broadcast')),
                ('expiration', models.DateField(verbose_name='expiration')),
                ('link', models.URLField(blank=True, null=True, verbose_name='link')),
                ('title', models.CharField(blank=True, max_length=1024, null=True, verbose_name='title')),
                ('description', models.TextField(blank=True, max_length=1024, null=True, verbose_name='description')),
                ('upload', models.DateTimeField(auto_now_add=True, verbose_name='upload')),
                ('dominant', models.CharField(blank=True, max_length=7, null=True, verbose_name='dominant')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('label', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='label')),
                ('content', tinymce.models.HTMLField(max_length=32768, verbose_name='content')),
            ],
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/newsletter', verbose_name='newsletter')),
                ('upload', models.DateTimeField(auto_now_add=True, verbose_name='upload')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='uploads/newsletter', verbose_name='thumbnail')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=256, verbose_name='area')),
                ('names', models.CharField(max_length=256, verbose_name='names (separated by comma)')),
                ('email', models.CharField(max_length=256, verbose_name='emails (separated by comma)')),
                ('ext', models.CharField(max_length=256, verbose_name='extention (separated by comma)')),
            ],
        ),
    ]
