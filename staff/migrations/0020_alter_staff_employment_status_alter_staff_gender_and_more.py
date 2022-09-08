# Generated by Django 4.1 on 2022-08-30 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0019_alter_staff_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='employment_status',
            field=models.CharField(choices=[('', '----'), ('PROBATION', 'Probation'), ('TEMPORARY', 'Temporary'), ('PERMANENT', 'Permanent')], max_length=30),
        ),
        migrations.AlterField(
            model_name='staff',
            name='gender',
            field=models.CharField(choices=[('', '----'), ('FEMALE', 'Female'), ('MALE', 'Male')], default='MALE', max_length=30),
        ),
        migrations.AlterField(
            model_name='staff',
            name='identification',
            field=models.CharField(choices=[('', '----'), ('PVC', 'Voters Card'), ('NIN', 'National ID'), ('LICENCE', 'Drivers Licence')], max_length=30),
        ),
        migrations.AlterField(
            model_name='staff',
            name='job_description',
            field=models.CharField(choices=[('', '----'), ('DRIVER', 'Driver'), ('SECURITY', 'Security'), ('MACHINE OPERATOR', 'Machine Operator'), ('NYSC', 'NYSC'), ('IT/SIWES', 'IT/SIWES')], max_length=50),
        ),
        migrations.AlterField(
            model_name='staff',
            name='relationship',
            field=models.CharField(choices=[('', '----'), ('PARENT', 'Parent'), ('SIBLING', 'Sibling'), ('SPOUSE', 'Spouse')], max_length=30),
        ),
    ]