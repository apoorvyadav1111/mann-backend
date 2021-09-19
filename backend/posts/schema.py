import graphene
import django_filters
from graphene import relay,ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Connection, ConnectionField, Node, Int
from graphql import GraphQLError
from graphql_jwt.decorators import login_required

from users.models import User
from posts.models import Post, PostStats
from backend.utils import global_id_to_primary_id
from activity.schema import ReactionNode

class PostFilter(django_filters.FilterSet):
	pk = django_filters.NumberFilter(field_name='pk',lookup_expr='exact')
	class Meta:
		model = Post
		#for model fields
		fields = {
		'id':['exact'],
		'user__id':['exact'],
		'user__username':['exact'],
		'title':['icontains','startswith'],
		'content':['icontains'],
		'tags':['icontains'],
		}
		# for non model fields
		filter_fields = {
		'pk':['exact']
		}

class PostNode(DjangoObjectType):
	pk = graphene.ID(source='pk',required=True)

	class Meta:
		model = Post		
		fields = ('id','pk','user','title','content','tags','created_at','poststats','comments','reactions','shares')	
		
		# to be removed after testing 
		'''
		filter_fields = {
		'id':['exact'],
		'pk':['exact'],
		'user__id':['exact'],
		'user__username':['exact'],
		'title':['icontains','startswith'],
		'content':['icontains'],
		'tags':['icontains'],
		}'''
		interfaces = (graphene.relay.Node,)

# Trying to add a custom field that will send 
# whether the user logged in have reacted to the post 
# or not.
# later we need to add if yes then what is the reaction

	is_reacted = graphene.Boolean()
	logged_reaction_id = graphene.ID()
	logged_reaction = graphene.Field(ReactionNode)

	@staticmethod
	def resolve_is_reacted(root, info, **kwargs):
		return len(root.reactions.filter(user=info.context.user))==1

	@staticmethod
	def resolve_logged_reaction_id(root,info,**kwargs):
		if bool(len(root.reactions.filter(user=info.context.user))==1):
			id = root.reactions.get(user=info.context.user).id
			#print("Node id: ", ReactionNode.get_node_id(id))
			return ReactionNode.get_node_id(id)

	@staticmethod
	def resolve_logged_reaction(root,info,**kwargs):
		if bool(len(root.reactions.filter(user=info.context.user))==1):
			id = root.reactions.get(user=info.context.user).id
			print(ReactionNode.get_node_id(id))
			return ReactionNode.get_node(info,(ReactionNode.get_node_id(id)))


class RelayCreatePost(relay.ClientIDMutation):
	post = graphene.Field(PostNode)

	class Input:
		title = graphene.String(required=True)
		content = graphene.String(required=True)
		tags = graphene.String(required=True)

		# to be removed after testing 
		# user have to be taken from login info
		# anonymous users will not be able to create posts

		user = graphene.ID()

	@classmethod
	@login_required
	def mutate_and_get_payload(cls,root,info,title,content,tags,user=None,**kwargs):
		user = info.context.user.id
		user = User.objects.get(id=user)

		try:
			post = Post(
				user=user,
				title=title,
				content=content,
				tags=tags)
			post.save()
			return RelayCreatePost(post=post)
		except Exception as e:
			return e

class RelayUpdatePost(relay.ClientIDMutation):
	post = graphene.Field(PostNode)
	message = graphene.String()
	class Input:
		id = graphene.ID(required=True)
		title = graphene.String()
		content = graphene.String()
		tags = graphene.String()

	@classmethod
	def mutate_and_get_payload(cls,root,info,id,**kwargs):
		if len(kwargs)==0:
			return RelayUpdatePost(message="Not found anything to update")
		if info.context.user.is_authenticated:
			user_id = info.context.user.id
			user = User.objects.get(id=user_id)
			node_type, id = global_id_to_primary_id(id)
			try:
				post = Post.objects.get(id=id)
				if user == post.user:
					for key, value in kwargs.items():
						setattr(post,key,value)
					post.save()
					return RelayUpdatePost(post=post, message="Post have been updated successfully")
				else:
					raise GraphQLError('You must be the owner of the post to edit it.')
			except Exception as e:
				return RelayUpdatePost(post=post, message=e)
		else:
			raise GraphQLError('You must be logged in to update a post')



class RelayDeletePost(relay.ClientIDMutation):
	post = graphene.Field(PostNode)
	message = graphene.String()

	class Input:
		id = graphene.ID(required=True)

	@classmethod
	def mutate_and_get_payload(cls,root,info,id):
		if info.context.user.is_authenticated:
			user = info.context.user.id
			user = User.objects.get(id=user)
			node_type, id = global_id_to_primary_id(id)
			try:
				post = Post.objects.get(id=id)
				if user == post.user:
					post.delete()
					return RelayDeletePost(message="Post has been deleted")
				else:
					raise GraphQLError('You must be the owner of the post to edit it.')
			except Exception as e:
				return RelayDeletePost(message=str(e))
		else:
			raise GraphQLError('You must be logged in to delete a post')


class PostStatsNode(DjangoObjectType):
	class Meta:
		model = PostStats
		fields = ('id','post','reacts','comments','shares','lastupdate')

		filter_fields ={
		'id':['exact']
		}

		interfaces = (graphene.relay.Node,)



class PostQuery(graphene.ObjectType):
	post = relay.Node.Field(PostNode)
	all_posts = DjangoFilterConnectionField(PostNode,filterset_class=PostFilter)

	poststats = relay.Node.Field(PostStatsNode)
	all_poststats = DjangoFilterConnectionField(PostStatsNode) #not required for now

class PostMutation(graphene.ObjectType):
	relay_create_post = RelayCreatePost.Field()
	relay_delete_post = RelayDeletePost.Field()
	relay_update_post = RelayUpdatePost.Field()