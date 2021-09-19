import graphene
from graphene import relay,ObjectType
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Connection,ConnectionField, Node,Int
from graphql_jwt.decorators import login_required
from graphql import GraphQLError

from users.models import User, UserProfile, Follow
from backend.utils import global_id_to_primary_id

class UserFilter(django_filters.FilterSet):
	pk = django_filters.NumberFilter(field_name='pk', lookup_expr='exact')

	class Meta:
		model = User

		#for model fields
		fields = {
		'id':['exact','icontains'],
		'username':['exact','icontains','startswith'],
		}

		# for non model fields
		filter_fields = {
		'pk':['exact']
		}

class UserNode(DjangoObjectType):
	pk = graphene.ID(source='pk',required=True)

	class Meta:
		model = User
		fields = ('id','pk','username','email','phone_number','first_name','last_name','date_joined',)

		# to be removed after testing 
		'''
		filter_fields = {
		'pk':['exact'],
		'id':['exact','icontains'],
		'username':['exact','icontains','startswith'],
		}
		'''
		interfaces = (relay.Node,)

class UserProfileNode(DjangoObjectType):
	class Meta:
		model = UserProfile
		fields = ('user','postcount','followingcount','followercount','last_update')

		filter_fields = {
		'user__id':['exact'],
		'user__username':['exact','icontains'],
		}
		interfaces = (relay.Node,)


class FollowNode(DjangoObjectType):
	class Meta:
		model = Follow
		fields = ('id','user','followsuser','followingstatus')

		filter_fields = {
		'id' : ['exact'],
		'user__username': ['exact','icontains'],
		'user__id' : ['exact'],
		'followsuser__id':['exact'],
		'followsuser__username':['exact','icontains']
		}

		interfaces = (relay.Node,)

class RelayCreateUser(relay.ClientIDMutation):
	user = graphene.Field(UserNode)

	class Input:
		email = graphene.String(required=True)
		username = graphene.String(required=True)
		password = graphene.String(required=True)

		#optional from Abstract User
		first_name = graphene.String()
		last_name = graphene.String()
		phone_number = graphene.String()
		is_staff = graphene.Boolean()
		is_active = graphene.Boolean()

	@classmethod
	def mutate_and_get_payload(cls,root,info,email,phone_number,username,**kwargs):
		user = User(
			username=username,
			email=email,
			phone_number=phone_number,
			**kwargs
			)
		user.set_password(kwargs['password'])
		user.save()

		return RelayCreateUser(user=user)
 
class RelayCreateFollow(relay.ClientIDMutation):
	follow = graphene.Field(FollowNode)
	message = graphene.String()

	class Input:
		
		# to be removed after testing
		# user = graphene.Int(required=True)
		# followsuser = graphene.Int(required=True)
		#

		# changed from user as a parameter to
		# user from info.context object
		# user = graphene.ID(required=True)
		followsuser = graphene.ID(required=True)

	
	@classmethod
	@login_required
	def mutate_and_get_payload(cls,root,info,followsuser,user=None,**kwargs):
		user = info.context.user.id
		user = User.objects.get(id=user)
		
		#u_node_type, uid = global_id_to_primary_id(user)
		#user = User.objects.get(id=uid)

		f_node_type, fid = global_id_to_primary_id(followsuser)
		followsuser = User.objects.get(id=fid)
		
		try:
			follow = Follow(
				user=user,
				followsuser=followsuser,
				followingstatus=True
				)
			follow.save()

			return RelayCreateFollow(follow=follow)
		except Exception as e:
			return RelayCreateFollow(message="Cannot Follow user right now, Please try again")

class RelayUpdateFollow(relay.ClientIDMutation):
	follow =  graphene.Field(FollowNode)
	message = graphene.String()

	class Input:
		followingstatus = graphene.Boolean(required=True)
		follow = graphene.ID(required=True)

	@classmethod
	@login_required
	def mutate_and_get_payload(cls,root,info,follow,followingstatus,**kwargs):
		user = info.context.user.id
		user = User.objects.get(id=user)

		f_node_type, fid= global_id_to_primary_id(follow)

		try:
			follow_object = Follow.objects.get(id=fid)

			if user == follow_object.user:
				follow_object.followingstatus = followingstatus
				follow_object.save()
				return RelayUpdateFollow(follow=follow_object,message="Updated Successfully!")
			else:
				raise GraphQLError('You must be owner of the this object to update it.')
		except Exception as e:
			return RelayUpdateFollow(message="Cannot update the following status, Please try again later.")

class RelayUpdateUser(relay.ClientIDMutation):
	user = graphene.Field(UserNode)
	message = graphene.String()

	class Input:
		first_name = graphene.String()
		last_name = graphene.String()
		is_active = graphene.Boolean()
		username = graphene.String()
		phone_number = graphene.String()

		# to-do: implement pwd update using mutation
		# password = graphene.String()
		# to-do: end

	@classmethod
	@login_required
	def mutate_and_get_payload(cls,root,info,**kwargs):
		if len(kwargs)==0:
			return RelayUpdateUser(user=user, message="Nothing to update")
		user = info.context.user.id
		user = User.objects.get(id=user)
		try:
			for key, value in kwargs.items():
				setattr(user,key,value)
			user.save()
			return RelayUpdateUser(user=user, message="Details updated successfully.")
		except Exception as e:
			return RelayUpdateUser(user=user, message="Cannot update, Please try again later.")

class RelayMutation(graphene.ObjectType):
	relay_create_user = RelayCreateUser.Field()
	relay_create_follow = RelayCreateFollow.Field()

	relay_update_follow = RelayUpdateFollow.Field()
	relay_update_user = RelayUpdateUser.Field()
	
class UserQuery(graphene.ObjectType):
	users = relay.Node.Field(UserNode)
	all_users  = DjangoFilterConnectionField(UserNode,filterset_class=UserFilter)
	
	def resolve_users_pages(root,info,**kwargs):
		return User.objects.all()

class FollowQuery(graphene.ObjectType):
	follow = relay.Node.Field(FollowNode)
	all_follows = DjangoFilterConnectionField(FollowNode)

class UserProfileQuery(graphene.ObjectType):
	userprofile = relay.Node.Field(UserProfileNode)
	all_userprofiles = DjangoFilterConnectionField(UserProfileNode)

'''

use this peice of code for changing relay id to id
then remove requirement of pk
to create while using relay

def get_form_kwargs(cls, root, info, **input):
    kwargs = {"data": input}

    global_id = input.pop("id", None)
    if global_id:
        node_type, pk = from_global_id(global_id)
        instance = cls._meta.model._default_manager.get(pk=pk)
        kwargs["instance"] = instance

    return kwargs

'''