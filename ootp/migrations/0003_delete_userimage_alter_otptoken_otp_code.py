# Generated by Django 5.1.6 on 2025-04-08 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ootp', '0002_alter_otptoken_otp_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserImage',
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='09ef7e', max_length=6),
        ),
    ]
