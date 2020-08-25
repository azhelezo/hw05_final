# Generated by Django 2.2.9 on 2020-07-11 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200711_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.CharField(default='-пусто-', max_length=200),
        ),
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(default='-пусто-', unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(default='-пусто-', max_length=200),
        ),
    ]