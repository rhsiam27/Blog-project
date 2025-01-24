from django.db import models
# from PIL import Image
# from django.contrib.auth.models import User
from django.utils.timezone import now
from taggit.managers import TaggableManager
from core import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category,related_name='post_set')
    tags = TaggableManager()
    img = models.ImageField(upload_to='post_img/',default='default.jpg')
    



    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username + ":"+ self.text[0:10]

