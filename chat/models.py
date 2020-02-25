from django.db import models
from django.utils import timezone


class ChatRoom(models.Model):
    name = models.TextField()
    label = models.TextField(unique=True)

    def __str__(self):
        return self.label


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages')
    handle = models.EmailField()
    message = models.TextField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}