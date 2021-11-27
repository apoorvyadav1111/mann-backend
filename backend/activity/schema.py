import graphene
from graphene import relay,ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Connection,ConnectionField,Node,Int
from graphql import GraphQLError
#from graphene.relay.Node import from_global_id

from activity.models import Comment,Reaction, Share
from users.models import User
from posts.models import Post
from backend.utils import global_id_to_primary_id

class CommentNode(DjangoObjectType):
	class Meta:
		model = Comment
		fields = ('id','post','user','commented_at','commentText','parent','replies')

		filter_fields = {
		'id':['exact'],
		'post__id':['exact'],
		'user__id':['exact'],
		'user__username':['exact'],
		'commentText':['icontains'],
		'parent__id':['exact','isnull'],
		'parent':['isnull']
		}

		interfaces = (graphene.relay.Node,)

class RelayCreateComment(relay.ClientIDMutation):
	comment = graphene.Field(CommentNode)
	message = graphene.String()

	class Input:
		
		# to be removed after testing
		#post = graphene.Int(required=True)
		#user = graphene.Int(required=True)
		#
		
		#user = graphene.ID(required=True)
		
		post = graphene.ID(required=True)
		commentText = graphene.String(required=True)

		# OPTIONAL FIELDS #
		parent_old = graphene.Int(required=False) # to be removed after testing the new one with ID type
		parent = graphene.ID()	

	@classmethod
	def mutate_and_get_payload(self,root,info,post,commentText,user=None,**kwargs):
		if info.context.user.is_authenticated:
			user = info.context.user.id
			user = User.objects.get(id=user)

			try:
				p_node_type, pid = global_id_to_primary_id(post)
				post = Post.objects.get(id=pid)

				#u_node_type, uid = global_id_to_primary_id(user)
				#user = User.objects.get(id=uid)

				if kwargs.get('parent_old'):
					parent = kwargs.get('parent_old')					
					parent = Comment.objects.get(id=parent)
					comment = Comment(
						user=user,
						post=post,
						parent=parent,
						commentText=commentText
						)

				elif kwargs.get('parent'):
					parent = kwargs.get('parent')
					parent_node_type, parent_id = global_id_to_primary_id(parent)
					parent = Comment.objects.get(id=parent_id)

					comment = Comment(
						user=user,
						post=post,
						parent=parent,
						commentText=commentText
						)
				else:
					comment = Comment(
						user=user,
						post=post,
						commentText=commentText
						)
				comment.save()
				return RelayCreateComment(comment=comment)
			except Exception as e:
				print(e)
				return RelayCreateComment(message="Cannot comment right now, please try again later.")
		else:
			raise GraphQLError('You must be logged in to comment on a post.')


class REACTION_CHOICES_ENUM(graphene.Enum):
	LIKE = "like"
	LOVE = "love"
	SUPPORT = "support"
	INSPIRE = "inspire"
	HAPPY = "happy"
	SAD = "sad"


class ReactionNode(DjangoObjectType):
	reaction = REACTION_CHOICES_ENUM()

	class Meta:
		model = Reaction
		fields = ('id','pk','post','user','reacted_at','reaction')

		filter_fields = {
		'id':['exact'],
		'user__id':['exact'],
		'user__username':['exact'],
		'post__id':['exact'],
		'reaction':['exact','icontains'],
		}

		#convert_choices_to_enum = ["reaction"]
		interfaces = (graphene.relay.Node,)


	def resolve_reaction_display(self,info,**kwargs):
		return self.get_reaction_display()

	@classmethod
	def get_node_id(cls, id):
		return graphene.relay.Node.to_global_id(cls._meta.name,id)

	@classmethod
	def get_node(cls, info, id):
		return cls(id=id)


class RelayCreateReaction(relay.ClientIDMutation):
	reaction = graphene.Field(ReactionNode)
	message = graphene.String()

	class Input:
		post = graphene.ID(required=True)

		# have changed the user from being sent as a variable
		# instead we take the user from context object	
		# user = graphene.ID(required=True)

		user = graphene.ID()
		
		reaction = REACTION_CHOICES_ENUM(required=True)


	@classmethod
	def mutate_and_get_payload(self,root,info,post,reaction,user=None,**kwargs):
		if info.context.user.is_authenticated:
			user = info.context.user.id
			user = User.objects.get(id=user)

			try:
				#u_node_type, uid = global_id_to_primary_id(user)
				p_node_type, pid = global_id_to_primary_id(post)
				post = Post.objects.get(id=pid)

				reaction = Reaction(
					user=user,
					post=post,
					reaction=reaction,
					**kwargs)
				reaction.save()
				return RelayCreateReaction(reaction=reaction, message="created successfully!")
			except Exception as e:
				return RelayCreateReaction(message="Unable to react right now, Please try again later.")
		else:
			raise GraphQLError('You must be logged in to react to a post.')

class ShareNode(DjangoObjectType):
	class Meta:
		model = Share
		fields = ('id','post','user','shared_at')

		filter_fields = {
		'id':['exact'],
		'user__id':['exact'],
		'user__username':['exact'],
		'post__id':['exact'],
		}

		interfaces = {graphene.relay.Node,}

class RelayCreateShare(relay.ClientIDMutation):
	share = graphene.Field(ShareNode)
	message = graphene.String()
	class Input:
		
		# to be removed after testing
		#post = graphene.Int(required=True)
		#user = graphene.Int(required=True)
		#
		post = graphene.ID(required=True)

		#user = graphene.ID(required=True)

	# to-do:start
	# user has to be removed from the parameters after testing.
	# to-do:end
	@classmethod
	def mutate_and_get_payload(self,root,info,post,user=None,**kwargs):
		if info.context.user.is_authenticated:
			user = info.context.user.id
			user = User.objects.get(id=user)

			try:
				p_node_type, pid = global_id_to_primary_id(post)
				#u_node_type, uid = global_id_to_primary_id(user)
				#user = User.objects.get(id=uid)

				post = Post.objects.get(id=pid)
				share = Share(
					post=post,
					user=user,
					**kwargs)
				share.save()
				return RelayCreateShare(share, message="Shared successfully")
			except Exception as e:
				return RelayCreateShare(message="Cannot share the post right now, Please try again later.")
		else:
			raise GraphQLError('You must be logged in to share the post')

class RelayUpdateReaction(relay.ClientIDMutation):
	reaction =  graphene.Field(ReactionNode)
	message = graphene.String()

	class Input:
		id = graphene.ID(required=True)
		reaction = REACTION_CHOICES_ENUM(required=True)	

	@classmethod
	def mutate_and_get_payload(cls,root,info,id,reaction):
		if info.context.user.is_authenticated:
			user = info.context.user.id
			user = User.objects.get(id=user)
			
			node_type, id = global_id_to_primary_id(id)
			try:
				reaction_object = Reaction.objects.get(id=id)
				if user == reaction_object.user:
					reaction_object.reaction = reaction
					reaction_object.save()
					return RelayUpdateReaction(reaction=reaction_object,message="Reaction has been updated successfully!")
				else:
					raise GraphQLError('You must be the owner of the reaction to edit it.')
			except Exception as e:
				return RelayUpdateReaction(message="Reaction cannot be updated, Please try again later.")
		else:
			raise GraphQLError('You must be logged in to update reaction on the post.')


class RelayUpdateComment(relay.ClientIDMutation):
	comment = graphene.Field(CommentNode)
	message = graphene.String()

	class Input:
		id = graphene.ID(required=True)
		commentText = graphene.String(required=True)

	@classmethod
	def mutate_and_get_payload(cls, root,info, id, **kwargs):
		if info.context.user.is_authenticated:
			user = info.context.user.id
			user = User.objects.get(id=user)

			node_type, id = global_id_to_primary_id(id)	
			try:
				comment_object = Comment.objects.get(id=id)
				if user == comment_object.user:
					comment_object.commentText = kwargs['commentText']
					comment_object.save()
					return RelayUpdateComment(comment=comment_object, message='Comment have been updated.')
				else:
					raise GraphQLError('You must be owner of the comment to update it.')
			except Exception as e:
				return RelayUpdateComment(comment=comment_object, message='Cannot update the comment,Try again later.')
		else:
			raise GraphQLError('You must be logged in to update the comment.')	


class RelayDeleteComment(relay.ClientIDMutation):
	comment = graphene.Field(CommentNode)
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
				comment = Comment.objects.get(id=id)

				# Only owner of the post or the comment can delete
				# the comment. This is to allow the author a certain
				# authority to maintain the decorum

				if user == comment.user or user == comment.post.user:
					comment.delete()
					return RelayDeleteComment(message="Comment have been deleted")
				else:
					raise GraphQLError('You must be the owner of either comment or post to delete the comment.')
			except Exception as e:
				return RelayDeleteComment(message="Comment cannot be deleted, Please try again later.")
		else:
			raise GraphQLError('You must be logged in to delete the conmment.')

class RelayDeleteReaction(relay.ClientIDMutation):
	reaction = graphene.Field(ReactionNode)
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
				reaction = Reaction.objects.get(id=id)
				if user == reaction.user:
					reaction.delete()
					return RelayDeleteReaction(message="Reaction have been deleted.")
				else:
					raise GraphQLError('You must be the owner of the reaction to delete it.')
			except Exception as e:
				return RelayDeleteReaction(reaction=reaction, message="Reaction cannot be deleted, Please try again later")
		else:
			raise GraphQLError('You must be logged in to delete the reaction.')

class RelayDeleteShare(relay.ClientIDMutation):
	share = graphene.Field(ShareNode)
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
				share = Share.objects.get(id=id)
				if user == share.user:
					share.delete()
					return RelayDeleteShare(message="Share has been deleted")
				else:
					raise GraphQLError('You must be owner of the shared object to delete it.')
			except Exception as e:
				#print(e)
				return RelayDeleteShare(share=share, message="Share cannot be deleted, Please try again later")
		else:
			raise GraphQLError('You must be logged in to delete shared post')




class ActivityQuery(graphene.ObjectType):
	comment = relay.Node.Field(CommentNode)
	all_comments = DjangoFilterConnectionField(CommentNode)

	def resolve_all_comments(root,info,**kwargs):
		return Comment.objects.filter(parent=None)

	reaction = relay.Node.Field(ReactionNode)
	all_reactions = DjangoFilterConnectionField(ReactionNode)

	share = relay.Node.Field(ShareNode)
	all_shares = DjangoFilterConnectionField(ShareNode)

class ActivityMutation(graphene.ObjectType):
	relay_create_comment = RelayCreateComment.Field()
	relay_create_reaction = RelayCreateReaction.Field()
	relay_create_share = RelayCreateShare.Field()

	relay_delete_comment = RelayDeleteComment.Field()
	relay_delete_share = RelayDeleteShare.Field()
	relay_delete_reaction = RelayDeleteReaction.Field()

	relay_update_comment = RelayUpdateComment.Field()
	relay_update_reaction = RelayUpdateReaction.Field()