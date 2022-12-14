from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


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
    image = models.ImageField("image", upload_to='static/images', default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title}, {self.author}'


class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=30)
    pub_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}, {self.author}'
