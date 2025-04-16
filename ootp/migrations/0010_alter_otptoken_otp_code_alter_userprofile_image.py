# Generated by Django 5.1.6 on 2025-04-11 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ootp', '0009_alter_otptoken_otp_code_userprofile_delete_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='c003d7', max_length=6),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
