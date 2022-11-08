# Generated by Django 4.1.3 on 2022-11-08 08:45

from django.db import migrations, models
import snsapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('snsapp', '0003_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=snsapp.models.image_directory_path),
        ),
    ]
