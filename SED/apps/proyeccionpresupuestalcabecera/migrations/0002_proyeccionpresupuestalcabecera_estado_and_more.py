# Generated by Django 4.0.2 on 2022-07-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyeccionpresupuestalcabecera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyeccionpresupuestalcabecera',
            name='estado',
            field=models.CharField(default='Procesado', max_length=50),
        ),
        migrations.AddField(
            model_name='proyeccionpresupuestalcabecera',
            name='objeto',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
