# Generated by Django 5.1.6 on 2025-04-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ootp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='bda91d', max_length=6),
        ),
    ]
