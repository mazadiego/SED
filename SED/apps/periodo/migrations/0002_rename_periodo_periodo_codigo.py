# Generated by Django 4.0.2 on 2022-03-18 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('periodo', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='periodo',
            old_name='periodo',
            new_name='codigo',
        ),
    ]
