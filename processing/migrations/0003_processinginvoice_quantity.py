# Generated by Django 3.2.13 on 2022-04-22 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0002_processinginvoice_processingsale'),
    ]

    operations = [
        migrations.AddField(
            model_name='processinginvoice',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
    ]