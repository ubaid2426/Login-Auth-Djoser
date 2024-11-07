# Generated by Django 4.2.16 on 2024-11-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0007_donationhistory_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationhistory',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
