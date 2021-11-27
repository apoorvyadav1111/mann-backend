from rest_framework import serializers
from posts.models import Post
from activity.serializers import CommentSerializer


class ParentComments(serializers.RelatedField):
	def to_representation(self,obj):
		if obj.parent is None:
			return CommentSerializer(obj).data
		else:
			return {}
class PostSerializer(serializers.ModelSerializer):
	#all_comments = CommentSerializer(many=True)
	#comments = ParentComments(many=True,required=False,read_only=True)
	comments = serializers.SerializerMethodField('get_comments')

	class Meta:
		model = Post
		fields = ['user','title','content','created_at','tags','comments']

	def create(self,validated_data):
		return Post.objects.create(**validated_data)

	def update(self,instance,validated_data):
		instance.content = validated_data.get('content',instance.content)
		instance.created_at = validated_data.get('created_at',instance.created_at)
		instance.tags = validated_data.get('tags',instance.tags)
		instance.save()
		return instance

	def get_comments(self,obj):
		comm = obj.comments.filter(parent__isnull=True)
		print("we are here",comm)
		return CommentSerializer(comm,many=True,required=False).data