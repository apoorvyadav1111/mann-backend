import graphene
import graphql_jwt
from django.contrib.auth import get_user_model

from users.schema import UserNode
from users.schema import UserQuery,RelayMutation, UserProfileQuery, FollowQuery
from posts.schema import PostQuery,PostMutation
from activity.schema import ActivityQuery, ActivityMutation

class Query(UserQuery, UserProfileQuery, FollowQuery, PostQuery,ActivityQuery,graphene.ObjectType):
	logged_user = graphene.String()
	
	def resolve_logged_user(self, info):
		return str(info.context.user)

	me = graphene.Field(UserNode)
	users = graphene.List(UserNode)

	def resolve_users(self, info):
		return get_user_model().objects.all()

	def resolve_me(self, info):
		user = info.context.user
		if user.is_anonymous:
			raise Exception('Not logged in!')
		return user

class AllMutation(RelayMutation,PostMutation,ActivityMutation,graphene.ObjectType):
	token_auth = graphql_jwt.ObtainJSONWebToken.Field()
	verify_token = graphql_jwt.Verify.Field()
	refresh_token = graphql_jwt.Refresh.Field()
	pass

schema = graphene.Schema(query=Query,mutation=AllMutation)