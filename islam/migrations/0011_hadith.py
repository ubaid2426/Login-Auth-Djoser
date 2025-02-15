# Generated by Django 4.2.16 on 2024-12-07 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0010_nameallah'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hadith',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata_length', models.IntegerField()),
                ('arabic_title', models.CharField(max_length=255)),
                ('arabic_author', models.CharField(max_length=255)),
                ('arabic_introduction', models.TextField()),
                ('english_title', models.CharField(max_length=255)),
                ('english_author', models.CharField(max_length=255)),
                ('english_introduction', models.TextField()),
                ('hadith_id', models.IntegerField()),
                ('id_in_book', models.IntegerField()),
                ('chapter_id', models.IntegerField()),
                ('book_id', models.IntegerField()),
                ('arabic_hadith', models.TextField()),
                ('english_narrator', models.CharField(max_length=255)),
                ('english_text', models.TextField()),
            ],
        ),
    ]
