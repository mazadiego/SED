# Generated by Django 4.0.2 on 2022-03-05 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tercero', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='tercero',
            name='UK_tercero_unique',
        ),
        migrations.RenameField(
            model_name='tercero',
            old_name='tipoidentificacion',
            new_name='tipoidentificacionid',
        ),
        migrations.AddConstraint(
            model_name='tercero',
            constraint=models.UniqueConstraint(fields=('codigo', 'tipoidentificacionid'), name='UK_tercero_unique'),
        ),
    ]
