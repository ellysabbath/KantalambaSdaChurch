# Generated by Django 5.1.6 on 2025-04-13 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ootp', '0025_communicationleadercredentials_delete_communication_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='4941e0', max_length=6),
        ),
    ]
