"""Django Models"""
import uuid
import arrow
import requests
import os
from datetime import datetime, timedelta

from django.db import models
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files import File

from django_telegrambot.apps import DjangoTelegramBot

import logging

LOGGER = logging.getLogger('django')

upload_storage = FileSystemStorage(location=settings.STATIC_ROOT, base_url='/static')

TASK = 1
MEETING = 2

# HELPER

def get_group_photo(group_chat_id):
    # Try to get the telegram chat photo

    # Get chat object from Telegram API
    chat = DjangoTelegramBot.dispatcher.bot.get_chat(group_chat_id)

    LOGGER.info("Getting chat photo of {}".format(chat.title))

    if chat.photo is None:
        return None

    # Get photo url from Telegram API
    photo_file = chat.photo.get_small_file()

    LOGGER.info("Retrieved photo_file of size {}".format(photo_file.file_size))

    path = settings.MEDIA_ROOT+str(chat.id)+'.jpg'


    # Download to media folder
    photo_file.download(custom_path=path)

    # Open the file
    photo = File(open(path, 'rb'))

    # Remove the temporary file path
    os.remove(path)

    LOGGER.info(f'Group Photo is retrieved for {chat.title}')

    return File(photo)

def get_photo_url_else_avatar(photo_url, name):

    if photo_url is not None:
        response = requests.get(photo_url)
        image = response.content

        LOGGER.info("Retrieved user photo of size {}".format(len(image)))

        if len(image) > 42:
            return photo_url

    r = 'https://ui-avatars.com/api/?name={}'.format(
            '+'.join(name.split(' '))
            )

    return r

class UserSettings(models.Model):
    """Settings for a particular User"""
    pushNotifications = models.BooleanField(default=True)
    autoCreateMeetingReminder = models.BooleanField(default=True)
    defaultMeetingReminderTimedelta = models.DurationField(default=timedelta(hours=3))
    autoCreateTaskReminder = models.BooleanField(default=True)
    defaultTaskReminderTimedelta = models.DurationField(default=timedelta(hours=10))
    botDetailedViewOnDefault = models.BooleanField(default=False)

class User(models.Model):
    """User model for Teleteam"""
    user_id = models.IntegerField()
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64, null=True)
    photo_telegram_url = models.CharField(max_length=256, null=True)
    settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE, default=None, null=True)
    
    def __str__(self):
        return f"{self.user_id}:{self.username}"

    def full_name(self):
        if self.first_name is not None:
            if self.last_name is not None:
                return self.first_name + " " + self.last_name
            else:
                return self.first_name
        else:
            return self.username
    
    @property
    def photo_url(self):
        return get_photo_url_else_avatar(
            self.photo_telegram_url, 
            self.full_name()
            )

class Group(models.Model):
    """Group model for Teleteam"""
    group_chat_id = models.IntegerField()
    chat_title = models.CharField(max_length=50)
    members = models.ManyToManyField(User)
    photo = models.ImageField(upload_to='group-photos/', null=True, storage=upload_storage)
    def __str__(self):
        return f"{self.group_chat_id}:{self.chat_title}"

    @property
    def tasks(self):
        return self.task_set.all()
    
    @property
    def meetings(self):
        return self.meeting_set.all()

    @property
    def closest_deadline(self):
        if len(self.tasks) == 0:
            return None
        else:
            return self.task_set.filter(done=False).order_by('deadline').first().deadline

    @property
    def photo_url(self):
        photo = get_group_photo(self.group_chat_id)
        if photo is not None:
            if self.photo is not None:
                os.remove(self.photo.path)
            self.photo = photo
            self.save()
            return self.photo.url
        else:
            return None

class Task(models.Model):
    """Task model for Teleteam"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    assigned_users = models.ManyToManyField(User)
    deadline = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.title},{self.group},{self.deadline}"

class Meeting(models.Model):
    """Meeting model for Teleteam"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    time = models.DateTimeField(default=now)
    def __str__(self):
        return f"Meeting {self.title} at {self.time}"

class Reminder(models.Model):
    """Reminders for tasks or meetings"""
    task = models.ForeignKey(Task, null=True, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, null=True, on_delete=models.CASCADE)
    reminding_type = models.IntegerField(default=MEETING)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()

class TaskSession(models.Model):
    """Temporary Telegram Chat Sessions based on Chat ID"""
    chat_id = models.CharField(max_length=128)
    title = models.CharField(max_length=128)
    assigned_users = models.CharField(max_length=128)
    deadline = models.DateTimeField(default=now)

    def __str__(self):
        """Print string"""
        return "id: {}".format(self.chat_id)

class Poll(models.Model):
    """A Poll for a meeting"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def message(self):
        """Generates a Poll text for Telegram Messages, and a dictionary of value mapping"""
        msg = []
        chc = {}

        msg.append('📊'+ self.title)
        msg.append("")

        choices = Choice.objects.filter(poll=self).order_by('time')

        if not choices:
            msg.append("Empty Poll")
        else:
            for i, choice in enumerate(choices):
                chc[i] = choice
                msg.append(f"<b>{i}: </b>"
                           + arrow.get(choice.time).to('Asia/Singapore').format("HH:mm dddd, D MMM YYYY")
                           + " - "
                           + str(Vote.objects.filter(choice=choice).count())
                           + " votes"
                           + "\n"
                           + ", ".join(vote.user.username for vote in Vote.objects.filter(choice=choice))
                           + "\n"
                           )

        return (chc, '\n'.join(msg))

class Choice(models.Model):
    """Choices for a Date Poll"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    time = models.DateTimeField(default=now)

class Vote(models.Model):
    """Votes for a Poll"""
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
