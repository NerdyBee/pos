# Generated by Django 3.2.13 on 2022-04-30 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0005_auto_20220428_0701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplyreturn',
            name='item',
        ),
        migrations.RemoveField(
            model_name='supplyreturn',
            name='user',
        ),
        migrations.RemoveField(
            model_name='processingsale',
            name='cost',
        ),
        migrations.RemoveField(
            model_name='processingsale',
            name='price',
        ),
        migrations.DeleteModel(
            name='SupplyDamage',
        ),
        migrations.DeleteModel(
            name='SupplyReturn',
        ),
    ]