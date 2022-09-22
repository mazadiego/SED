# Generated by Django 4.0.2 on 2022-09-22 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institucioneducativa', '0003_alter_institucioneducativa_usuarioid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjuntos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipodocumento', models.IntegerField()),
                ('consecutivo', models.PositiveIntegerField()),
                ('nombrearchivo', models.CharField(max_length=500)),
                ('archivobase64', models.FileField(blank='', default='', upload_to='files/')),
                ('institucioneducativaid', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='institucioneducativa.institucioneducativa')),
            ],
        ),
    ]
