from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

#a custom manager to retrieve only the published posts
class PublishedManager(models.Manager):
    def get_quesryset(self):
        return super(PublishedManager,self).get_quesryset().filter(status='published')
    
class Post(models.Model):

    # A post model to store our posts
    POST_STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') #for seo friendly urls
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=POST_STATUS, default='draft')

    #our custom manager
    published = PublishedManager()

    #default manager
    objects = models.Manager()
 
    class Meta:
        # tell django to sort our data in descending prder when we quesry
        ordering = ('-publish',)
 
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail_view', args=[self.publish.year, self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])