from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    poster = models.ImageField(upload_to='movie-poster/')

    def __str__(self):
        return str(self.title)

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content_text = models.CharField(max_length=300)
    # integerfieldを選択式にするために選択肢を定義
    star_choices = [
        (0,'0 star'),
        (1,'1 star'),
        (2,'2 star'),
        (3,'3 star'),
        (4,'4 star'),
        (5,'5 star'),
        (6,'6 star'),
        (7,'7 star'),
        (8,'8 star'),
        (9,'9 star'),
        (10,'10 star'),
    ]
    star_num = models.IntegerField(default=0,choices=star_choices)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
