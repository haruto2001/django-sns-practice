# Generated by Django 4.1.3 on 2022-11-14 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import snsapp.models
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snsapp', '0004_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=stdimage.models.StdImageField(blank=True, force_min_size=False, null=True, upload_to=snsapp.models.image_directory_path, variations={'thumbnail': {'height': 500, 'width': 500}}),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='コメントを入力')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snsapp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
