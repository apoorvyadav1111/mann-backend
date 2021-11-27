from django.contrib import admin
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from django.conf.urls import url
import rest_auth as rest_auth
from users.views import UserViewSet
#from posts.views import PostViewSet
#from activity.views import ReactionViewSet,CommentViewSet,ShareViewSet
from graphene_django.views import GraphQLView
import rest_framework
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from backend.permissions import IsOwnerOrReadOnly
from graphql_jwt.decorators import jwt_cookie

class DRFAuthenticatedGraphQLView(GraphQLView):
    #permission_classes = [IsAuthenticated]
    def parse_body(self, request):
        if isinstance(request, rest_framework.request.Request):
            return request.data
        return super(DRFAuthenticatedGraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(DRFAuthenticatedGraphQLView, cls).as_view(*args, **kwargs)
        #view = permission_classes((IsAuthenticated,))(view)
        view = api_view(['GET', 'POST'])(view)
        return view

router = routers.DefaultRouter()
#router.register('user', UserViewSet)
#router.register('post',PostViewSet,basename='post')
#router.register('reaction',ReactionViewSet,basename='reaction')
#router.register('comment',CommentViewSet,basename='comment')
#router.register('share',ShareViewSet,basename='share')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^graphql_token', jwt_cookie(DRFAuthenticatedGraphQLView.as_view(graphiql=True))),
    url(r'^graphql$',csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
]