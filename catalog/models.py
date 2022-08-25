from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    status_choices = (
        ('deferred', 'Deferred'),
        ('published', 'Published'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='deferred')
    title = models.CharField(max_length=100)
    short_text = models.CharField(max_length=250)
    full_text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title, self.author


class Comment(models.Model):
    text = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.text, self.author
