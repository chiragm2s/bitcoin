# Generated by Django 3.2.8 on 2022-10-19 19:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bitcoin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitcoin',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]