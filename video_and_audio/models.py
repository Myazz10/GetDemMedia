from django.contrib.sessions.models import Session
from django.db import models
from django.utils import timezone


class Audio(models.Model):
    identifier = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=500, null=True, blank=True)
    publish_date = models.CharField(max_length=50, null=True, blank=True)
    views = models.CharField(max_length=100, null=True, blank=True)
    length = models.CharField(max_length=100, null=True, blank=True)
    api = models.CharField(max_length=50, null=True, blank=True)
    mp3 = models.FileField(upload_to='audios/', null=True, blank=True)
    downloaded_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name', '-downloaded_on']


class Video(models.Model):
    identifier = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    thumbnail = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=500, null=True, blank=True)
    publish_date = models.CharField(max_length=50, null=True, blank=True)
    views = models.CharField(max_length=100, null=True, blank=True)
    length = models.CharField(max_length=100, null=True, blank=True)
    api = models.CharField(max_length=50, null=True, blank=True)
    mp4 = models.FileField(upload_to='videos/', null=True, blank=True)
    downloaded_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['name', '-downloaded_on']


class ActivityPerSession(models.Model):
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)
    audio_count = models.IntegerField(default=0)
    video_count = models.IntegerField(default=0)
    overall_count = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session.session_key
