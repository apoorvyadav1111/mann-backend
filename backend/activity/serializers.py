from rest_framework import serializers
from activity.models import Reaction,Comment,Share

class ReactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Reaction
		fields = ['post','user','reacted_at','reaction']


class RepliesField(serializers.RelatedField):
	def to_representation(self,value):
		#return {'id':value.id,'commentText':value.commentText}
		return CommentSerializer(value).data


class CommentSerializer(serializers.ModelSerializer):
	post_author = serializers.CharField(source='post.user',read_only=True)
	commentator_name = serializers.CharField(source='user.username',read_only=True)
	replies = RepliesField(many=True,required=False,read_only=True)

	class Meta:
		model = Comment
		fields = ['parent','post','post_author','user','commentator_name','commented_at','commentText','replies']
	'''
	post_author = serializers.SerializerMethodField('get_author_name')

	def get_author_name(self,obj):
		return obj.post.user
   
	'''

class ShareSerializer(serializers.ModelSerializer):
	class Meta:
		model = Share
		fields = ['post','user','shared_at']
