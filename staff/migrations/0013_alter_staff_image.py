# Generated by Django 4.1 on 2022-08-25 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0012_alter_staff_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.ImageField(blank=True, default='images/default.png', upload_to='images'),
        ),
    ]
