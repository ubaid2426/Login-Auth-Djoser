# Generated by Django 4.2.16 on 2024-12-11 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0020_categoryselect_donationmodel_categoryselect'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donationmodel',
            old_name='categoryselect',
            new_name='category_select',
        ),
    ]
