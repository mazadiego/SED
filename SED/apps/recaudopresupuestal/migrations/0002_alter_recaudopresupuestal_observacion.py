# Generated by Django 4.0.2 on 2022-05-01 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recaudopresupuestal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recaudopresupuestal',
            name='observacion',
            field=models.CharField(max_length=5000),
        ),
    ]