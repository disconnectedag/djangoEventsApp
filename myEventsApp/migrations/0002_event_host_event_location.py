# Generated by Django 4.2.6 on 2023-10-22 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myEventsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.CharField(default='host', max_length=100),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
