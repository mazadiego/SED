# Generated by Django 4.0.2 on 2022-03-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyeccionpresupuestaldetalle', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='proyeccionpresupuestaldetalle',
            name='UK_proyeccionpresupuestalid_fuenterecuroid_rubropresupuestalid_unique',
        ),
        migrations.RenameField(
            model_name='proyeccionpresupuestaldetalle',
            old_name='fuenterecuroid',
            new_name='fuenterecursoid',
        ),
        migrations.AddConstraint(
            model_name='proyeccionpresupuestaldetalle',
            constraint=models.UniqueConstraint(fields=('proyeccionpresupuestalid', 'fuenterecursoid', 'rubropresupuestalid'), name='UK_proyeccionpresupuestalid_fuenterecursoid_rubropresupuestalid_unique'),
        ),
    ]
