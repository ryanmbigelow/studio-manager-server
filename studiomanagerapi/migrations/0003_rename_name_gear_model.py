# Generated by Django 4.1.3 on 2023-08-22 02:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studiomanagerapi', '0002_gear_engineer_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gear',
            old_name='name',
            new_name='model',
        ),
    ]