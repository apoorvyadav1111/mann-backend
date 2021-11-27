from django.shortcuts import render
from rest_framework import viewsets
from activity.serializers import ReactionSerializer, CommentSerializer, ShareSerializer
from activity.models import Reaction,Comment,Share
from django_filters.rest_framework import DjangoFilterBackend as filter

# Create your views here.
class ReactionViewSet(viewsets.ModelViewSet):
	serializer_class = ReactionSerializer
	model = Reaction

	queryset = model.objects.all()
	filter_backends = (filter,)
	filter_fields = ('post__id',)
	
class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	model = Comment

	queryset = model.all_objects.all()
	filter_backends = (filter,)
	filter_fields = ('post__id',)
	

class ShareViewSet(viewsets.ModelViewSet):
	serializer_class = ShareSerializer
	model = Share
	#permissions_class = [permissions.IsOwner] 
	#only post creater would be seeing all the shares

	queryset = model.objects.all()
	filter_backends = (filter,)
	filter_fields = ('post__id',)