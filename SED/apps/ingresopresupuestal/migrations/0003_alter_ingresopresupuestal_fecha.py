# Generated by Django 4.0.2 on 2022-04-20 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingresopresupuestal', '0002_alter_ingresopresupuestal_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingresopresupuestal',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
