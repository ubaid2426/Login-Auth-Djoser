# Generated by Django 4.2.16 on 2024-12-08 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0016_alter_hadith_english_narrator_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Hadith',
        ),
        migrations.DeleteModel(
            name='Metadata',
        ),
    ]
