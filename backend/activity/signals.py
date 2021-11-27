from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from activity.models import Reaction,Comment, Share
from posts.models import PostStats

#declare your signals here
#
@receiver(post_save,sender=Comment)
def update_post_comments(sender,created,instance,**kwargs):
	if created:
	    id = instance.post.poststats.id
	    stat = PostStats.objects.get(id=id)
	    stat.comments += 1
	    stat.save()

@receiver(post_delete,sender=Comment)
def decrement_post_comments(sender,instance,**kwargs):
	try:
		id = instance.post.poststats.id
		stat = PostStats.objects.get(id=id)
		stat.comments -= 1
		stat.save()
	except Exception as e:
		print(e)

@receiver(post_save,sender=Reaction)
def update_post_reactions(sender,created,instance,**kwargs):
    if created:
	    id = instance.post.poststats.id
	    stat = PostStats.objects.get(id=id)
	    stat.reacts += 1
	    stat.save()

@receiver(post_delete,sender=Reaction)
def decrement_post_reactions(sender,instance,**kwargs):
	try:
		id = instance.post.poststats.id
		stat = PostStats.objects.get(id=id)
		stat.reacts -= 1
		stat.save()
	except Exception as e:
		print(e)

@receiver(post_save,sender=Share)
def update_post_shares(sender,created,instance,**kwargs):
    if created:
	    id = instance.post.poststats.id
	    stat = PostStats.objects.get(id=id)
	    stat.shares += 1
	    stat.save()

@receiver(post_delete,sender=Share)
def decrement_post_shares(sender,instance,**kwargs):
	try:	
		id = instance.post.poststats.id
		stat = PostStats.objects.get(id=id)
		stat.shares -= 1
		stat.save()
	except Exception as e:
		print(e)