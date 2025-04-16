# Generated by Django 5.1.6 on 2025-04-15 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ootp', '0036_alter_communicationmaingoals_cost_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='treasurergoal',
            name='status',
            field=models.CharField(choices=[('choose status', 'choose status'), ('pending', 'pending'), ('on process', 'on process'), ('completed', 'completed')], default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='otptoken',
            name='otp_code',
            field=models.CharField(default='085764', max_length=6),
        ),
    ]
