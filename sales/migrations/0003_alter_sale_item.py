# Generated by Django 3.2.13 on 2022-04-22 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0004_alter_processingsale_item'),
        ('sales', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='processing.product'),
        ),
    ]
