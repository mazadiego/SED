# Generated by Django 4.0.2 on 2022-09-16 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudpresupuestalcabecera', '0004_alter_solicitudpresupuestalcabecera_observacion'),
        ('certificadodisponibilidadpresupuestal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificadodisponibilidadpresupuestal',
            name='rubropresupuestalid',
        ),
        migrations.AddField(
            model_name='certificadodisponibilidadpresupuestal',
            name='estado',
            field=models.CharField(default='Procesado', max_length=50),
        ),
        migrations.AddField(
            model_name='certificadodisponibilidadpresupuestal',
            name='objeto',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AddField(
            model_name='certificadodisponibilidadpresupuestal',
            name='solicitudpresupuestalcabeceraid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='solicitudpresupuestalcabecera.solicitudpresupuestalcabecera'),
        ),
    ]
