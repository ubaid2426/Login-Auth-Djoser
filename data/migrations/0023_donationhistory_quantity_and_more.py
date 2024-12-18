# Generated by Django 4.2.16 on 2024-12-18 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0022_allcategorymodel_category_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationhistory',
            name='quantity',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='donationhistory',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
