# Generated by Django 4.2.16 on 2024-11-06 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_remove_donationmodel_donation_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationhistory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='payment_images/'),
        ),
    ]
