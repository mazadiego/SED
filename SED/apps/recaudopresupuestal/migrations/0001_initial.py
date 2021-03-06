# Generated by Django 4.0.2 on 2022-04-20 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tiporecaudo', '0001_initial'),
        ('institucioneducativa', '0003_alter_institucioneducativa_usuarioid'),
        ('ingresopresupuestal', '0002_alter_ingresopresupuestal_fecha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recaudopresupuestal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consecutivo', models.PositiveIntegerField()),
                ('fecha', models.DateField()),
                ('documentorecaudo', models.CharField(max_length=500)),
                ('observacion', models.CharField(blank=True, max_length=5000)),
                ('valor', models.DecimalField(decimal_places=6, max_digits=18)),
                ('ingresopresupuestalid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ingresopresupuestal.ingresopresupuestal')),
                ('institucioneducativaid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='institucioneducativa.institucioneducativa')),
                ('tiporecaudoid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tiporecaudo.tiporecaudo')),
            ],
        ),
        migrations.AddConstraint(
            model_name='recaudopresupuestal',
            constraint=models.UniqueConstraint(fields=('institucioneducativaid', 'consecutivo'), name='UK_recaudopresupuestal_institucioneducativaid_consecutivo_unique'),
        ),
    ]
