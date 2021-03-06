# Generated by Django 4.0.2 on 2022-05-27 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registropresupuestal', '0001_initial'),
        ('institucioneducativa', '0003_alter_institucioneducativa_usuarioid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Obligacionpresupuestal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consecutivo', models.PositiveIntegerField()),
                ('fecha', models.DateField()),
                ('recibosatisfacion', models.PositiveIntegerField()),
                ('observacion', models.CharField(max_length=500)),
                ('valor', models.DecimalField(decimal_places=6, max_digits=18)),
                ('institucioneducativaid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='institucioneducativa.institucioneducativa')),
                ('registropresupuestalid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='registropresupuestal.registropresupuestal')),
            ],
        ),
        migrations.AddConstraint(
            model_name='obligacionpresupuestal',
            constraint=models.UniqueConstraint(fields=('institucioneducativaid', 'consecutivo'), name='UK_OP_institucioneducativaid_consecutivo_unique'),
        ),
    ]
