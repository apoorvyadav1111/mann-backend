from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
		Custom permission to allow only owner of the object
		to edit it
	"""

	def has_object_permission(self,request, view, obj):
		# if request methods are GET, HEAD & OPTIONS
		# we will allow the users
		if request.method in permissions.SAFE_METHODS:
			return True
		# process anonymous request later
		#if not request.user.is_authenticated:
		#	return False
			
		# for all other request we will 
		return obj.owner == request.user