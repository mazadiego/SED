# Generated by Django 4.0.2 on 2022-04-13 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institucioneducativa', '0003_alter_institucioneducativa_usuarioid'),
        ('tercero', '0002_remove_tercero_uk_tercero_unique_and_more'),
        ('fuenterecurso', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingresopresupuestal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consecutivo', models.PositiveIntegerField()),
                ('fecha', models.DateTimeField()),
                ('observacion', models.CharField(blank=True, max_length=5000)),
                ('valor', models.DecimalField(decimal_places=6, max_digits=18)),
                ('fechaproyeccionrecaudo', models.DateField()),
                ('fuenterecursoid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='fuenterecurso.fuenterecurso')),
                ('institucioneducativaid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='institucioneducativa.institucioneducativa')),
                ('terceroid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tercero.tercero')),
            ],
        ),
        migrations.AddConstraint(
            model_name='ingresopresupuestal',
            constraint=models.UniqueConstraint(fields=('institucioneducativaid', 'consecutivo'), name='UK_institucioneducativaid_consecutivo_unique'),
        ),
    ]
