# Generated by Django 4.0.2 on 2022-03-05 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tipoidentificacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tercero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=500)),
                ('tipoidentificacion', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tipoidentificacion.tipoidentificacion')),
            ],
        ),
        migrations.AddConstraint(
            model_name='tercero',
            constraint=models.UniqueConstraint(fields=('codigo', 'tipoidentificacion'), name='UK_tercero_unique'),
        ),
    ]
