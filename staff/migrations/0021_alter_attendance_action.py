# Generated by Django 4.1 on 2022-08-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0020_alter_staff_employment_status_alter_staff_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='action',
            field=models.CharField(choices=[('', '----'), ('CHECKIN', 'Checkin'), ('BREAKOUT', 'Breakout'), ('BREAKIN', 'Breakin'), ('CHECKOUT', 'Checkout')], max_length=255),
        ),
    ]
