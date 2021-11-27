from posts.models import Post 
from users.models import User, Follow, UserProfile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_user_profile(sender,created,instance,**kwargs):
    if created:
        UserProfile.objects.create(user=User.objects.get(id=instance.id))


@receiver(post_save,sender=Post)
def increment_post_count(sender,created,instance,**kwargs):
    if created:
        a = UserProfile.objects.get(user=instance.user)
        a.postcount += 1
        a.save()

@receiver(post_save,sender=Follow)
def increment_follow_count(sender,instance,**kwargs):
    a = UserProfile.objects.get(user=instance.user)
    b = UserProfile.objects.get(user=instance.followsuser)

    if instance.followingstatus == True:
        a.followingcount += 1
        b.followercount += 1
        a.save()
        b.save()

    elif instance.followingstatus == False:
        a.followingcount -= 1
        b.followercount -= 1
        a.save()
        b.save()