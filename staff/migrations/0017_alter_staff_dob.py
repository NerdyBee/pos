# Generated by Django 4.1 on 2022-08-28 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0016_alter_staff_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
