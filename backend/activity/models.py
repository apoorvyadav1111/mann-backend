from django.db import models
from posts.models import Post
from users.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

from posts.models import PostStats
from backend.settings.base import AUTH_USER_MODEL


# Create your models here.
class Reaction(models.Model):

	# CHANGES TO BE DONE -
	# 1
	# REACTION WOULD BE CHANGED FROM CHARFIELD  
	# TO CHOICES - COMPLETED
	#
	# 2
	# A POST AND USER SHOULD BE UNIQUE TOGETHER
	# TO UPDATE THIS CONSTRAINT
	# RIGHT NOW A PERSON CAN CREATE MULTIPLE REACTIONS - COMPLTETED
	# 
	# 3 
	# CAN WE QUERY WHETHER A USER HAVE REACTED ON A POST?
	

	class REACTION_CHOICES(models.TextChoices):
		LIKE = "like"
		LOVE = "love"
		SUPPORT = "support"
		INSPIRE = "inspire"
		HAPPY = "happy"
		SAD = "sad"
		

	post = models.ForeignKey(Post,related_name='reactions',on_delete=models.CASCADE)
	user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
	reacted_at = models.DateTimeField(auto_now_add=True)
	reaction = models.CharField(
		max_length=10,
		choices=REACTION_CHOICES.choices,
		default=REACTION_CHOICES.LIKE
		)

	class Meta:
		unique_together = ('user', 'post')

	def __str__(self):
		return self.reaction

class CommentManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()

class ParentCommentManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset()

class Comment(models.Model):
	post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
	user = models.ForeignKey(AUTH_USER_MODEL,related_name='comments',on_delete=models.CASCADE)
	commented_at = models.DateTimeField(auto_now_add=True)
	commentText = models.TextField()
	parent = models.ForeignKey('self',null=True,blank=True,related_name='replies',on_delete=models.CASCADE)
	objects = ParentCommentManager()
	all_objects = CommentManager()

	class Meta:
		ordering = ('commented_at',)

	def __str__(self):
		return self.commentText

class Share(models.Model):
	post = models.ForeignKey(Post,related_name='shares',on_delete=models.CASCADE)
	user = models.ForeignKey(AUTH_USER_MODEL,related_name='shares',on_delete=models.CASCADE)
	shared_at = models.DateTimeField(auto_now_add=True)

'''
# signals have been migrated to signals module
# to be deleted 
@receiver(post_save,sender=Comment)
def update_post_comments(sender,instance,**kwargs):
    id = instance.post.poststats.id
    print("here id equals this ",id)
    stat = PostStats.objects.get(id=id)
    stat.comments += 1
    stat.save()

@receiver(post_delete,sender=Comment)
def decrement_post_comments(sender,instance,**kwargs):
	id = instance.post.poststats.id
	stat = PostStats.objects.get(id=id)
	stat.comments -= 1
	stat.save()


@receiver(post_save,sender=Reaction)
def update_post_reactions(sender,instance,**kwargs):
    id = instance.post.poststats.id
    stat = PostStats.objects.get(id=id)
    stat.reacts += 1
    stat.save()

@receiver(post_delete,sender=Reaction)
def decrement_post_reactions(sender,instance,**kwargs):
	id = instance.post.poststats.id
	stat = PostStats.objects.get(id=id)
	stat.reacts -= 1
	stat.save()


@receiver(post_save,sender=Share)
def update_post_shares(sender,instance,**kwargs):
    id = instance.post.poststats.id
    print("here id equals this ",id)
    stat = PostStats.objects.get(id=id)
    stat.shares += 1
    stat.save()

@receiver(post_delete,sender=Share)
def decrement_post_shares(sender,instance,**kwargs):
	id = instance.post.poststats.id
	stat = PostStats.objects.get(id=id)
	stat.shares -= 1
	stat.save()
'''