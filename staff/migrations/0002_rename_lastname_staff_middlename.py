# Generated by Django 4.1 on 2022-08-22 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='lastname',
            new_name='middlename',
        ),
    ]
