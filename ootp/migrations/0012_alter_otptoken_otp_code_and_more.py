# Generated by Django 5.1.6 on 2025-04-11 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ootp', '0011_allmembers_events_treasurer_zonehistory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='75ff48', max_length=6),
        ),
        migrations.AlterField(
            model_name='zonehistory',
            name='certificateStatus',
            field=models.CharField(choices=[('choose status', 'Choose status'), ('completed', 'Completed'), ('pending', 'Pending'), ('on process', 'On process')], default='', max_length=20),
        ),
    ]
