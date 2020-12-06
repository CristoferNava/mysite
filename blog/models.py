from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Each Django model has a least one manager to handle the data base, the default
# manager is called objects. 
# we can create custom managers 

# Manager to retrieve all posts with the published status
# Post.published.all()
class PublishedManager(models.Manager):
    # this method returns the QuerySet that will be executed.
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                                            .filter(status='published')

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

    objects = models.Manager() # the default manager
    published = PublishedManager() # Our custom manager.

    # get_absolute_url use to return a cononical URL for the object.
    # the reverse() method build URLs by their name and pass optional parameters
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                      args=[self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # each comment will be made on one post, and each post may have multiple comments
    # the related_name attribute allows you to name the attribute that you use
    # for the relationship from the related object back to this one
    # after defining this, we can retrieve the post of a comment object using comment.post
    # and also retrieve all comments of a post using post.comments.all()
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} of {self.post}'


