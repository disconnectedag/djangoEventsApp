# Generated by Django 4.2.6 on 2023-10-30 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myEventsApp', '0003_remove_event_imagelink_remove_event_imagename_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
