from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.PROTECT, related_name='topics')
    # related_name parameter will be used to create a reverse relationship
    # where the Board instances will have access a list of Topic instance
    # that belong to it
    starter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='topics')


class Post(models.Model):
    message = models.CharField(max_length=4000)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='+')
