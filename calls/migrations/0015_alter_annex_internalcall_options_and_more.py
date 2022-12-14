# Generated by Django 4.1.2 on 2022-12-02 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calls', '0014_annex_jointcall_annex_studentscall_result_jointcall_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='annex_internalcall',
            options={'verbose_name': 'Annex'},
        ),
        migrations.AlterModelOptions(
            name='annex_jointcall',
            options={'verbose_name': 'Annex'},
        ),
        migrations.AlterModelOptions(
            name='result_internalcall',
            options={'verbose_name': 'Result'},
        ),
        migrations.AlterModelOptions(
            name='result_jointcall',
            options={'verbose_name': 'Result'},
        ),
        migrations.AlterModelOptions(
            name='termsofreference_internalcall',
            options={'verbose_name': 'Terms of reference'},
        ),
        migrations.AlterModelOptions(
            name='termsofreference_jointcall',
            options={'verbose_name': 'Terms of reference'},
        ),
        migrations.AlterModelOptions(
            name='termsofreference_studentscall',
            options={'verbose_name': 'Terms of reference'},
        ),
        migrations.AlterModelOptions(
            name='timeline_jointcall',
            options={'verbose_name': 'Timeline'},
        ),
        migrations.AlterField(
            model_name='termsofreference_internalcall',
            name='terms_of_reference',
            field=models.FileField(blank=True, null=True, upload_to='uploads/calls_internal', verbose_name='terms of reference'),
        ),
        migrations.AlterField(
            model_name='termsofreference_jointcall',
            name='terms_of_reference',
            field=models.FileField(blank=True, null=True, upload_to='uploads/calls_join', verbose_name='terms of reference'),
        ),
        migrations.AlterField(
            model_name='termsofreference_studentscall',
            name='terms_of_reference',
            field=models.FileField(blank=True, null=True, upload_to='uploads/calls_student', verbose_name='terms of reference'),
        ),
        migrations.AlterField(
            model_name='timeline_internalcall',
            name='start_date',
            field=models.DateField(verbose_name='start date'),
        ),
        migrations.AlterField(
            model_name='timeline_jointcall',
            name='start_date',
            field=models.DateField(verbose_name='start date'),
        ),
    ]
