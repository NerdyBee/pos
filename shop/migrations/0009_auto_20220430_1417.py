# Generated by Django 3.2.13 on 2022-04-30 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_purchasesale_supplier_d'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchasesale',
            name='sale_type',
            field=models.CharField(choices=[('CS', 'Cash'), ('CR', 'Credit')], default='CS', max_length=10),
        ),
        migrations.AlterField(
            model_name='purchaseinvoice',
            name='sale_type',
            field=models.CharField(choices=[('CS', 'Cash'), ('CR', 'Credit')], max_length=10),
        ),
    ]