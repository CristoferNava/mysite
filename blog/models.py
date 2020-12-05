from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # unique_for_date for build URLs for posts using the publish date and slug
    # with this Django will prevent multiple posts from having the same slug field for 
    # a given date
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    # many-to-one relationship, each post is written by a user, and user can write any number of posts
    # Django will create a foreign key in the database using the primary key of the related model
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title