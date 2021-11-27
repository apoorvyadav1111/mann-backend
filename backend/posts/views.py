from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from posts.serializers import PostSerializer
from posts.models import Post
from django_filters.rest_framework import DjangoFilterBackend as filter


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	model = Post
	queryset = model.objects.all()

	filter_backends = (filter,)
	filter_fields = ('user__id','id')