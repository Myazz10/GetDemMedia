import os
from django.core.files import File
from moviepy.audio.io.AudioFileClip import AudioFileClip
from .models import TitleError, ErrorCharacter
from video_and_audio.models import Video, Audio, ActivityPerSession
from pytube import YouTube
from django.conf import settings


class YouTubeFox:
    def __init__(self, url, user_marker):
        self._title = ''
        self.filename = None
        self._url = url
        self._user = user_marker
        self._video_file = None
        self._audio_file = None
        self.video_details = {}
        self._video = None
        self._special_characters = None
        self._check_characters()

    def validate_link(self):
        valid = False

        try:
            self._video = YouTube(self._url)
            valid = True
        except:
            pass

        print(f'Valid link: {valid}\n')

        return valid

    def _get_details(self, force_download):
        request_amount = 0

        if force_download:
            print('Force downloading...')
            print('\nBefore of the while loop...')

            while True:
                flag = False

                try:
                    self._title = self._video.title

                    # Removing all special characters
                    print(f'Before: {self._title}')

                    translation = self._title.maketrans({i: "" for i in self._special_characters})
                    self.filename = self._title.translate(translation)

                    print(f'After: {self.filename}\n')

                    self._video_file = f'{self.filename}.mp4'

                    length = self._video.length
                    temp_length = str(length)

                    if len(str(length)) == 3:
                        length = temp_length[0] + ':' + temp_length[1:]
                    elif len(str(length)) == 4:
                        length = temp_length[:2] + ':' + temp_length[2:]
                    elif len(str(length)) == 5:
                        length = temp_length[0] + ':' + \
                                 temp_length[1:3] + ':' + temp_length[3:]

                    self.video_details['length'] = length
                    self.video_details['thumbnail'] = self._video.thumbnail_url
                    self.video_details['title'] = self._video.title
                    self.video_details['author'] = self._video.author
                    self.video_details['views'] = self._video.views
                    self.video_details['publish_date'] = self._video.publish_date.strftime("%b %d, %Y")

                    flag = True
                except:
                    request_amount += 1

                if flag or request_amount == 10:
                    print(f'Request amount: {request_amount} after break...')
                    break

            print('\nAfter of the while loop...')

        else:
            print('Regular downloading...')
            self._title = self._video.title

            # Removing all special characters
            print(f'Before: {self._title}')

            translation = self._title.maketrans({i: "" for i in self._special_characters})
            self.filename = self._title.translate(translation)

            print(f'After: {self.filename}\n')

            self._video_file = f'{self.filename}.mp4'

            length = self._video.length
            temp_length = str(length)

            if len(str(length)) == 3:
                length = temp_length[0] + ':' + temp_length[1:]
            elif len(str(length)) == 4:
                length = temp_length[:2] + ':' + temp_length[2:]
            elif len(str(length)) == 5:
                length = temp_length[0] + ':' + \
                         temp_length[1:3] + ':' + temp_length[3:]

            self.video_details['length'] = length
            self.video_details['thumbnail'] = self._video.thumbnail_url
            self.video_details['title'] = self._video.title
            self.video_details['author'] = self._video.author
            self.video_details['views'] = self._video.views
            self.video_details['publish_date'] = self._video.publish_date.strftime("%b %d, %Y")

        return request_amount

    def download(self, force_download=None, file_type='mp4'):
        http_404_error = True
        request_amount = 0

        try:
            request_amount = self._get_details(force_download)
            http_404_error = False
        except:
            pass

        print(f'API error: {http_404_error}')

        if not http_404_error or force_download:
            print('Video is downloading...')

            if force_download:
                # To prevent to HTTP 404 when downloading the object...
                while True:
                    flag = False

                    try:
                        if file_type == 'mp3':
                            self._video.streams.filter(only_audio=True).first().download()
                        else:
                            self._video.streams.get_highest_resolution().download()

                        flag = True
                    except:
                        request_amount += 1

                    if flag or request_amount == 20:
                        print(f'Request amount: {request_amount} after break...')
                        break
            else:
                try:
                    if file_type == 'mp3':
                        self._video.streams.filter(only_audio=True).first().download()
                    else:
                        self._video.streams.get_highest_resolution().download()
                except:
                    pass

            print('Video was downloaded successfully!\n')

        if request_amount == 20:
            return http_404_error, request_amount

        else:
            return http_404_error, None

    def get_video(self):
        created = False
        object_saved = False
        video = Video()

        try:
            video.mp4 = File(open(self._video_file, mode='rb'))

            print('File was successfully uploaded.')
            video.name = self._title
            video.api = 'PyTube API'
            video.thumbnail = self.video_details['thumbnail']
            video.author = self.video_details['author']
            video.publish_date = self.video_details['publish_date']
            video.views = str(self.video_details['views'])
            video.length = str(self.video_details['length'])

            try:
                video.identifier = str(self._user)
            except:
                print('Could not save the session ID as an identifier')

            try:
                video.save()
                object_saved = True
            except:
                print('Object was not saved!')

            if object_saved:
                try:
                    video.identifier = self._register_activity('mp4')
                    video.save()
                except:
                    print('Could not save the session ID as an identifier')

                # self._register_activity('mp4')

            created = True

        except Exception:
            print('File not found!')

        if created:
            return created, video

        else:
            return created, None

    def get_audio(self):
        created = False
        object_saved = False
        audio = Audio()

        self._audio_file = f'{self.filename}.mp3'

        clip = AudioFileClip(self._video_file)
        clip.write_audiofile(self._audio_file)
        clip.close()

        try:
            audio.mp3 = File(open(self._audio_file, mode='rb'))

            print('File was successfully uploaded.')
            audio.name = self._title
            audio.api = 'PyTube API'

            audio.thumbnail = self.video_details['thumbnail']
            audio.author = self.video_details['author']
            audio.publish_date = self.video_details['publish_date']
            audio.views = str(self.video_details['views'])
            audio.length = str(self.video_details['length'])

            try:
                audio.identifier = str(self._user)
            except:
                print('Could not save the session ID as an identifier')

            try:
                audio.save()
                object_saved = True
            except:
                print('Object was not saved!')

            if object_saved:
                try:
                    audio.identifier = self._register_activity('mp3')
                    audio.save()
                except:
                    print('Could not save the session ID as an identifier')

                # self._register_activity('mp3')

            created = True

        except Exception:
            print('File not found!')

        if created:
            return created, audio

        else:
            return created, None

    def clean_up(self):
        if self._audio_file:
            if self._audio_file in os.listdir(settings.BASE_DIR):
                try:
                    os.remove(self._audio_file)
                except:
                    pass

        if self._video_file in os.listdir(settings.BASE_DIR):
            try:
                os.remove(self._video_file)
            except:
                pass

            print('Delete downloaded file.')

    def _highlight_title(self):
        title = TitleError()
        title.name = self._video_file
        title.url = str(self._url)
        title.email_sender()
        title.save()

    def _check_characters(self):
        error_characters_lists = ErrorCharacter.objects.all()

        if not error_characters_lists.exists():
            self._special_characters = ['"', '.', ',', '$', '#', "'", '\\', '/', ':', ';', '|', '?']

            # Converting the list to a string to save it to the database
            error_characters = ", ".join(self._special_characters)

            errors = ErrorCharacter()
            errors.name = error_characters
            errors.save()
        else:
            # Converting the string back to a list to loop over it...
            self._special_characters = list(error_characters_lists.first().name.split(", "))

    def _register_activity(self, file_type):
        try:
            if ActivityPerSession.objects.filter(session=self._user).exists():
                print(f'Session exist: {self._user}')
                session_activity = ActivityPerSession.objects.get(session=self._user)
                # session_activity.session = self._user

                if file_type == 'mp4':
                    count = session_activity.video_count
                    count += 1
                    session_activity.video_count = count

                elif file_type == 'mp3':
                    count = session_activity.audio_count
                    count += 1
                    session_activity.audio_count = count

                total = session_activity.audio_count + session_activity.video_count
                session_activity.overall_count = total
                session_activity.save()

            else:
                print(f'Created session: {self._user}')
                session_activity = ActivityPerSession()
                session_activity.session = self._user

                if file_type == 'mp4':
                    count = session_activity.video_count
                    count += 1
                    session_activity.video_count = count

                elif file_type == 'mp3':
                    count = session_activity.audio_count
                    count += 1
                    session_activity.audio_count = count

                total = session_activity.audio_count + session_activity.video_count
                session_activity.overall_count = total
                session_activity.save()

            return session_activity

        except:
            print('Error for the session here...')

        return None
