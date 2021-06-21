from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from website.views import home, download_director, download_video, download_audio


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('download-director/', download_director, name="download-director"),
    path('download-video/', download_video, name="download-video"),
    path('download-audio/', download_audio, name="download-audio"),
]

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# To facilitate the uploads of media files to the website... To help create the media url for an image file.
'''if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)'''
