# Generated by Django 4.0.2 on 2022-07-20 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyeccionpresupuestalcabecera', '0003_alter_proyeccionpresupuestalcabecera_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyeccionpresupuestalcabecera',
            name='estado',
            field=models.CharField(default='Por Aprobar', max_length=50),
        ),
    ]
