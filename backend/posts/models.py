from django.db import models
from users.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from backend.settings.base import AUTH_USER_MODEL

#Create you model managers here
class PostManager():
    def create_post(self,user,content,created_at,tags):
        post = self.model(
            user=user,
            content=content,
            tags=tags)
        post.save(using=self._db)


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,related_name='post',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.TextField()
    objects = PostManager()
    
    def __str__(self):
        return self.title


class PostStats(models.Model):
    post = models.OneToOneField(Post,related_name='poststats',on_delete=models.CASCADE)
    reacts = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    lastupdate = models.DateTimeField(auto_now=True)
