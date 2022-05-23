# Generated by Django 4.0.2 on 2022-05-16 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tercero', '0002_remove_tercero_uk_tercero_unique_and_more'),
        ('institucioneducativa', '0003_alter_institucioneducativa_usuarioid'),
        ('certificadodisponibilidadpresupuestal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registropresupuestal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consecutivo', models.PositiveIntegerField()),
                ('fecha', models.DateField()),
                ('observacion', models.CharField(max_length=500)),
                ('valor', models.DecimalField(decimal_places=6, max_digits=18)),
                ('certificadodisponibilidadpresupuestalid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='certificadodisponibilidadpresupuestal.certificadodisponibilidadpresupuestal')),
                ('institucioneducativaid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='institucioneducativa.institucioneducativa')),
                ('terceroid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='tercero.tercero')),
            ],
        ),
        migrations.AddConstraint(
            model_name='registropresupuestal',
            constraint=models.UniqueConstraint(fields=('institucioneducativaid', 'consecutivo'), name='UK_RP_institucioneducativaid_consecutivo_unique'),
        ),
    ]
