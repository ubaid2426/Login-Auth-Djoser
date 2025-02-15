# Generated by Django 4.2.18 on 2025-02-01 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0018_metadata_hadith'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuaCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.TextField()),
                ('arabic_text', models.TextField()),
                ('dua', models.TextField()),
                ('urdu_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EventCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urdu_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HadithCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.TextField()),
                ('urdu_text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='HolyPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='holy_places/')),
                ('description', models.TextField()),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VerseCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.TextField()),
                ('arabic_text', models.TextField()),
                ('urdu_text', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='hadith',
            name='english_narrator',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='arabic_author',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='arabic_title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='english_author',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='english_title',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='length',
            field=models.TextField(null=True),
        ),
    ]
