# Generated by Django 4.0.2 on 2022-03-17 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.BigIntegerField(unique=True)),
                ('activo', models.BooleanField()),
            ],
        ),
    ]