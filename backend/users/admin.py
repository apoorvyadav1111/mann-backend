from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User,Follow,UserProfile


class UserAccountAdmin(UserAdmin):

    def full_name(self, obj):
        return obj.get_full_name()

    list_display = (
        'username',
        'email',
        'phone_number',
        'full_name',
        'password',
        'date_joined',
    )

class FollowAdmin(admin.ModelAdmin):

	def full_name(self,obj):
		return obj.get_full_name()
	list_display = (
		'user',
		'followsuser',
		'followingstatus',
		'created_at'
	)

class UserProfileAdmin(admin.ModelAdmin):

	def full_name(self,obj):
		return obj.get_full_name()

	list_display = (
		'user',
		'postcount',
		'followercount',
		'followingcount',
		'last_update'
	)

admin.site.register(User, UserAccountAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
