# Generated by Django 4.0 on 2022-01-09 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(default='news-1'),
        ),
    ]
