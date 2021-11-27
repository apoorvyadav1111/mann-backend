# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from posts.models import Post,PostStats

# Register your models here.

class PostAdmin(admin.ModelAdmin):

    def full_name(self, obj):
        return obj.get_full_name()

    list_display = (
        'user',
        'title',
        'content',
        'created_at',
        'tags',
    )

class PostStatsAdmin(admin.ModelAdmin):

    def full_name(self, obj):
        return obj.get_full_name()

    list_display = (
        'post',
        'reacts',
        'comments',
        'shares',
        'lastupdate',
    )


admin.site.register(Post,PostAdmin)
admin.site.register(PostStats,PostStatsAdmin)