# Generated by Django 4.1 on 2022-08-25 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0011_staff_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.ImageField(default='images/default.png', null=True, upload_to='images'),
        ),
    ]