# Generated by Django 3.2.15 on 2023-02-07 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dima', '0007_auto_20221205_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment_Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='Nombre del archivo')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='uploads/content', verbose_name='Adjunto')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='dima.content')),
            ],
            options={
                'verbose_name': 'Adjunto',
            },
        ),
    ]