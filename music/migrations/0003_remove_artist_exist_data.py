# Generated by Django 4.0 on 2022-01-05 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_mediatype_member_alter_genre_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='exist_data',
        ),
    ]