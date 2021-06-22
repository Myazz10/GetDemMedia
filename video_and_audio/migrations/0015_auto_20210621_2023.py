# Generated by Django 3.2.4 on 2021-06-22 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_and_audio', '0014_auto_20210621_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='mp3',
            field=models.FileField(blank=True, null=True, upload_to='audios/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='mp4',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
