# Generated by Django 4.2.16 on 2024-11-30 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0009_alter_verse_options_alter_verse_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameAllah',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('eng_name', models.CharField(max_length=255)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='imgs/')),
                ('eng_meaning', models.CharField(max_length=255)),
                ('explanation', models.TextField()),
            ],
        ),
    ]
