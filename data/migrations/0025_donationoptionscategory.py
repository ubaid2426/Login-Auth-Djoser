# Generated by Django 4.2.16 on 2024-12-20 19:45

import data.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0024_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationOptionsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('category', models.ForeignKey(default=data.models.get_default_category1, on_delete=django.db.models.deletion.CASCADE, related_name='donations_option', to='data.category')),
                ('category_select', models.ForeignKey(default=data.models.get_default_category1, on_delete=django.db.models.deletion.CASCADE, related_name='donation_sselect', to='data.categoryselect')),
            ],
        ),
    ]
