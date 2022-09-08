# Generated by Django 3.2.13 on 2022-05-24 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0007_remove_supplysale_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processinginvoice',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='processingsale',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='supply',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='supply',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='supplysale',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]