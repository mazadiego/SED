# Generated by Django 4.0.2 on 2022-08-28 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modificacionproyeccionpresupuestaldetalle', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='modificacionproyeccionpresupuestaldetalle',
            name='UK_modificacionproyeccionpresupuestalid_fuenterecursoid_rubropresupuestalid_unique',
        ),
    ]