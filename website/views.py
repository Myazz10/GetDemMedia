from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from .pytube_api import YouTubeFox
from website.comments import get_comments
import secrets


def home(request):
    debug = settings.DEBUG

    try:
        marker_key = request.session['marker_key']

    except:
        marker_key = secrets.token_hex(16)
        request.session['marker_key'] = str(marker_key)

    today = datetime.now()
    context = {
        'debug': debug,
        'user_marker': str(marker_key),
    }

    result = True

    if request.method == 'POST':
        submission_form = request.POST.get('submission')

        if submission_form == 'url-form':
            search_url = request.POST.get('search')
            checked_radio = request.POST.get('file-type')
            force_download = request.POST.get('force-download')

        elif submission_form == 'comment-form':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            get_comments(name, email, message)
            success_comment = f"Hi {name.title()}, thanks for the contact! We'll get back to you soon."
            context['success_comment'] = success_comment

    context['result'] = result
    context['current_year'] = today.year

    return render(request, 'website/home.html', context)


def download_director(request):
    context = {
        'url': request.POST.get('url'),
        'file_format': request.POST.get('file_format'),
        'user_marker': request.POST.get('user_marker'),
        'force_download': request.POST.get('force_download'),
    }
    return JsonResponse(context)


def download_video(request):
    context = {}

    # Because these has been retrieved via the GET method... They have been passed as an array/list respectively...
    url = request.GET.get('url'),
    file_format = request.GET.get('file_format'),
    user_marker = request.GET.get('user_marker'),
    force_download = request.GET.get('force_download'),

    context['url'] = url[0]
    context['file_format'] = file_format[0]
    context['user_marker'] = user_marker[0]
    context['force_download'] = force_download[0]

    fox = YouTubeFox(url[0], user_marker[0])

    if not fox.validate_link():
        context['invalid_url'] = 'This is not a valid YouTube url... Get a valid url please!'

    else:
        api_error, request_amount = fox.download(force_download[0])
        # api_error, request_amount = fox.download()

        if request_amount == 20:
            context['timeout'] = f'{request_amount} amount of requests has been sent in the ' \
                                 f'background and none was successful. The API is down at this time. '

        else:
            if not api_error:
                result, video = fox.get_video()

                if video:
                    context['video_url'] = video.mp4.url
                    context['title'] = fox.video_details['title']
                    context['thumbnail'] = fox.video_details['thumbnail']
                    context['author'] = fox.video_details['author']
                    context['publish_date'] = video.publish_date
                    context['views'] = fox.video_details['views']
                    context['length'] = fox.video_details['length']

                    fox.clean_up()

                else:
                    context['special_characters_flag'] = 'This video url cannot be converted right now. Please ' \
                                                         'try again in 24 hours. You may also try another ' \
                                                         'url now. '
            else:
                context['api_error'] = 'There is an API error here! Please retry...'

    return JsonResponse(context)


def download_audio(request):
    context = {}

    # Because these has been retrieved via the GET method... They have been passed as an array/list respectively...
    url = request.GET.get('url'),
    file_format = request.GET.get('file_format'),
    user_marker = request.GET.get('user_marker'),
    force_download = request.GET.get('force_download'),

    context['url'] = url[0]
    context['file_format'] = file_format[0]
    context['user_marker'] = user_marker[0]
    context['force_download'] = force_download[0]

    fox = YouTubeFox(url[0], user_marker[0])

    if not fox.validate_link():
        context['invalid_url'] = 'This is not a valid YouTube url... Get a valid url please!'
    else:
        api_error, request_amount = fox.download(force_download[0], 'mp3')

        if request_amount == 20:
            context['timeout'] = f'{request_amount} amount of requests has been sent in the ' \
                                 f'background and none was successful. The API is down at this time. '

        else:
            if not api_error:
                result, audio = fox.get_audio()

                if audio:
                    context['audio_url'] = audio.mp3.url
                    context['title'] = fox.video_details['title']
                    context['thumbnail'] = fox.video_details['thumbnail']
                    context['author'] = fox.video_details['author']
                    context['publish_date'] = audio.publish_date
                    context['views'] = fox.video_details['views']
                    context['length'] = fox.video_details['length']

                    fox.clean_up()

                else:
                    context['special_characters_flag'] = 'This video url cannot be converted right now. Please ' \
                                                         'try again in 24 hours. You may also try another url ' \
                                                         'now. '
            else:
                context['api_error'] = 'There is an API error here! Please retry...'
    return JsonResponse(context)
