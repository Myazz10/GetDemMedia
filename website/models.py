from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail


class AnimatedHeaderText(models.Model):
    first_paragraph = models.CharField(max_length=50, null=True, blank=True)
    second_paragraph = models.CharField(max_length=50, null=True, blank=True)
    third_paragraph = models.CharField(max_length=50, null=True, blank=True)
    fourth_paragraph = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'Animated Header Text'


class WebsiteName(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)


class PermitPlaylistDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Approved by {self.user.username.title()}'


class MyazzDesignzProfile(models.Model):
    website = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    pinterest = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'Myazz Designz Contacts'


class TitleError(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    error_date = models.DateTimeField(default=timezone.now)

    # Will be sending the email.
    def email_sender(self):
        subject = 'Get Dem Media - Title Error Needs Fixing'
        message = f'Please to check on the following link - Name: {self.name}, URL: {self.url}... Maybe it is an ' \
                  f'urgent situation! \nFILE NOT FOUND WHERE IT WAS DOWNLOADED!'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently = False)

    def __str__(self):
        return f'{self.name}'


class ErrorCharacter(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}'


class Notice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    when = models.DateTimeField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name.title()}'


class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField(null=True, blank=True)
    date_commented = models.DateTimeField(default=timezone.now)

    subject = models.CharField(max_length=100)
    reply = models.TextField(null=True, blank=True)
    replied = models.BooleanField(default=False)
    date_replied = models.DateTimeField(default=timezone.now)

    # Overriding the save method to send email
    def save(self, *args, **kwargs):
        # Send the email if the replied box has been checked.
        if self.replied:
            self.email_sender()

        super(Comment, self).save(*args, **kwargs)

    # Will be sending the email.
    def email_sender(self):
        self.date_replied = timezone.now()
        # send_mail(self.subject, self.reply, EMAIL_HOST_USER, [self.email], fail_silently = False)

    def __str__(self):
        return self.name
