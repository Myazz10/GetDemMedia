from django.contrib import admin
from .models import Audio, Video, ActivityPerSession
from django.contrib.sessions.models import Session


admin.site.register(Session)


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    search_fields = ['name', 'api', 'downloaded_on']
    list_filter = ['name', 'api', 'downloaded_on']
    list_display = ['name', 'api', 'downloaded_on']
    list_per_page = 30


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    search_fields = ['name', 'api', 'downloaded_on']
    list_filter = ['name', 'api', 'downloaded_on']
    list_display = ['name', 'api', 'downloaded_on']
    list_per_page = 30


@admin.register(ActivityPerSession)
class ActivityPerSessionAdmin(admin.ModelAdmin):
    search_fields = ['session_key', 'audio_count', 'video_count', 'overall_count', 'last_activity']
    list_display = ['session_key', 'audio_count', 'video_count', 'overall_count', 'last_activity']
    list_per_page = 100

    def session_key(self, obj):
        return f'{obj.session}'

    session_key.short_description = "Session Key"
