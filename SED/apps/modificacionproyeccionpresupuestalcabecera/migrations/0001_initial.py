# Generated by Django 4.0.2 on 2022-07-19 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institucioneducativa', '0003_alter_institucioneducativa_usuarioid'),
        ('periodo', '0002_rename_periodo_periodo_codigo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modificacionproyeccionpresupuestalcabecera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.CharField(blank=True, max_length=5000)),
                ('objeto', models.CharField(default='', max_length=5000)),
                ('estado', models.CharField(default='Procesado', max_length=50)),
                ('institucioneducativaid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='institucioneducativa.institucioneducativa')),
                ('periodoid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='periodo.periodo')),
            ],
        ),
        migrations.AddConstraint(
            model_name='modificacionproyeccionpresupuestalcabecera',
            constraint=models.UniqueConstraint(fields=('periodoid', 'institucioneducativaid'), name='UK_periodo_institucioneducativa_MPP_unique'),
        ),
    ]
