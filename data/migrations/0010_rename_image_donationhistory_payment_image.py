# Generated by Django 4.2.16 on 2024-11-07 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_donationhistory_donor_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donationhistory',
            old_name='image',
            new_name='Payment_image',
        ),
    ]
