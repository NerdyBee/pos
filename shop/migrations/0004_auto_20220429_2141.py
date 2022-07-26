# Generated by Django 3.2.13 on 2022-04-29 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('suppliers', '0002_alter_supplydeposit_sale_type'),
        ('shop', '0003_auto_20220428_0650'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier', models.CharField(max_length=255)),
                ('invoice_no', models.IntegerField()),
                ('sale_type', models.CharField(choices=[('CS', 'Cash'), ('CR', 'Credit')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('supplier_d', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='suppliers.suppliers')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SupplierSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.IntegerField()),
                ('quantity', models.IntegerField(null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('cost', models.IntegerField(blank=True, default=0, null=True)),
                ('sale_type', models.CharField(choices=[('CS', 'Cash'), ('CR', 'Credit')], max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.inventory')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='otherincome',
            name='user',
        ),
        migrations.RemoveField(
            model_name='outbank',
            name='user',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='item',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='user',
        ),
        migrations.RemoveField(
            model_name='promoinvoice',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='promoinvoice',
            name='user',
        ),
        migrations.RemoveField(
            model_name='promosale',
            name='item',
        ),
        migrations.RemoveField(
            model_name='promosale',
            name='user',
        ),
        migrations.RemoveField(
            model_name='purchasereturn',
            name='item',
        ),
        migrations.RemoveField(
            model_name='purchasereturn',
            name='user',
        ),
        migrations.RemoveField(
            model_name='salesreturn',
            name='item',
        ),
        migrations.RemoveField(
            model_name='salesreturn',
            name='user',
        ),
        migrations.DeleteModel(
            name='Damage',
        ),
        migrations.DeleteModel(
            name='OtherIncome',
        ),
        migrations.DeleteModel(
            name='OutBank',
        ),
        migrations.DeleteModel(
            name='Promo',
        ),
        migrations.DeleteModel(
            name='PromoInvoice',
        ),
        migrations.DeleteModel(
            name='PromoSale',
        ),
        migrations.DeleteModel(
            name='PurchaseReturn',
        ),
        migrations.DeleteModel(
            name='SalesReturn',
        ),
    ]
