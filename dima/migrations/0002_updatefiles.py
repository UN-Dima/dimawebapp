# Generated by Django 4.2 on 2023-11-20 19:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dima", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UpdateFiles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "table_to_update",
                    models.CharField(
                        help_text="Base de Datos a Actualizar",
                        max_length=256,
                        verbose_name="Tabla",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="uploads/updates", verbose_name="Archivo"
                    ),
                ),
                ("upload_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
