# Generated by Django 4.0.2 on 2022-08-06 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recaudopresupuestal', '0002_alter_recaudopresupuestal_observacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='recaudopresupuestal',
            name='estado',
            field=models.CharField(default='Procesado', max_length=50),
        ),
        migrations.AddField(
            model_name='recaudopresupuestal',
            name='objeto',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
