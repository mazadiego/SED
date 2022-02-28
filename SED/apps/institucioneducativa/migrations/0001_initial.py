# Generated by Django 4.0.2 on 2022-02-26 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institucioneducativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=50, unique=True)),
                ('nombre', models.CharField(max_length=500)),
                ('usuarioid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.usuario')),
            ],
        ),
    ]
