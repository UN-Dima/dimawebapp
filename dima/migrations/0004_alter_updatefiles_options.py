# Generated by Django 4.2 on 2023-11-20 19:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("dima", "0003_alter_updatefiles_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="updatefiles",
            options={
                "verbose_name": "Actualizar XLS",
                "verbose_name_plural": "Actualizaciónes de XLS",
            },
        ),
    ]