# Generated by Django 3.2.13 on 2022-04-29 22:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0002_alter_supplydeposit_sale_type'),
        ('shop', '0004_auto_20220429_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseinvoice',
            name='customer_d',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='suppliers.suppliers'),
        ),
    ]
