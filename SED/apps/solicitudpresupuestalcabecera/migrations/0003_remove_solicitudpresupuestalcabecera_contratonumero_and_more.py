# Generated by Django 4.0.2 on 2022-09-15 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudpresupuestalcabecera', '0002_solicitudpresupuestalcabecera_estado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitudpresupuestalcabecera',
            name='contratonumero',
        ),
        migrations.RemoveField(
            model_name='solicitudpresupuestalcabecera',
            name='fechafincontrato',
        ),
        migrations.RemoveField(
            model_name='solicitudpresupuestalcabecera',
            name='fechainiciocontrato',
        ),
        migrations.RemoveField(
            model_name='solicitudpresupuestalcabecera',
            name='terceroid',
        ),
        migrations.RemoveField(
            model_name='solicitudpresupuestalcabecera',
            name='tipocontratoid',
        ),
    ]