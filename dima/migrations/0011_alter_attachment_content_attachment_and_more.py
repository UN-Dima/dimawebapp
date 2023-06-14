# Generated by Django 4.2 on 2023-05-08 21:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dima", "0010_alter_attachment_content_attachment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attachment_content",
            name="attachment",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="uploads/content",
                verbose_name="Adjunto",
            ),
        ),
        migrations.AlterField(
            model_name="broadcast",
            name="image",
            field=models.FileField(
                upload_to="uploads/broadcast", verbose_name="Imagen para difusión"
            ),
        ),
        migrations.AlterField(
            model_name="newsletter",
            name="file",
            field=models.FileField(
                upload_to="uploads/newsletter", verbose_name="Boletín"
            ),
        ),
        migrations.AlterField(
            model_name="newsletter",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="uploads/newsletter"
            ),
        ),
    ]
