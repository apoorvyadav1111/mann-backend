# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from activity.models import Reaction,Comment,Share

class ReactionAdmin(admin.ModelAdmin):

    def full_name(self, obj):
        return obj.get_full_name()

    list_display = (
    	'post',
        'get_author',
   		'user',
    	'reaction',
    	'reacted_at',
    )

    def get_author(self,obj):
    	return obj.post.user
    get_author.short_description = 'Post Creator'
    get_author.admin_order_field = 'author'

class CommentAdmin(admin.ModelAdmin):

    def full_name(self,obj):
        return obj.get_full_name()

    list_display = (
        'post',
        'get_author',
        'parent',
        'user',
        'commentText',
        'commented_at',
    )

    def get_author(self,obj):
        return obj.post.user
    get_author.short_description = 'Post Creator'
    get_author.admin_order_field = 'author'
    
    def get_queryset(self,request):
        return self.model.all_objects.all()

class ShareAdmin(admin.ModelAdmin):

    def full_name(self,obj):
        return obj.get_full_name()

    list_display = (
        'post',
        'get_author',
        'user',
        'shared_at',
    )

    def get_author(self,obj):
        return obj.post.user
    get_author.short_description = 'Post Creator'
    get_author.admin_order_field = 'author'

# Register your models here.
admin.site.register(Reaction,ReactionAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Share,ShareAdmin) 