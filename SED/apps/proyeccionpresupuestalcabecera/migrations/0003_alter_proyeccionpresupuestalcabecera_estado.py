# Generated by Django 4.0.2 on 2022-07-20 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyeccionpresupuestalcabecera', '0002_proyeccionpresupuestalcabecera_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyeccionpresupuestalcabecera',
            name='estado',
            field=models.CharField(blank=True, default='Por Aprobar', max_length=50),
        ),
    ]
