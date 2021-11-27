from posts.models import Post, PostStats
from django.db.models.signals import post_save
from django.dispatch import receiver

#signal to create a poststat object for our post

@receiver(post_save,sender=Post)
def create_post_stats(sender,created,instance,**kwargs):
    if created:
        PostStats.objects.create(post=instance)
