# Generated by Django 4.2 on 2023-07-19 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dima', '0014_attachment_content_area_attachment_content_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment_content',
            name='tipo',
        ),
        migrations.AddField(
            model_name='attachment_content',
            name='type',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Tipo'),
        ),
    ]
